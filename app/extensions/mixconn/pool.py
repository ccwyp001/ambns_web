# -*- coding: utf-8 -*-

import copy
import contextlib
import collections
import logging
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import threading
import time
import cx_Oracle
import datetime
import paramiko
from .exception import (
    DBUnSupportedError, DBConnectionError,
    DBExecutionError, GroupExhaustedError,
    SSHConnectionError, SSHExecutionError,
    SSHScriptExecutionError)

log = logging.getLogger(__name__)


class ConnectionFactory(object):
    TIME_OUT = 5

    def _oracle(host, port, database, user, pswd, timeout):
        dsn = cx_Oracle.makedsn(host, port, database)
        return cx_Oracle.connect(user, pswd, dsn, threaded=True)

    def _ssh(host, port, _none, user, pswd, timeout):
        client = paramiko.SSHClient()
        # Allow to connect to host which doesn't exist in known_hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=user, password=pswd, timeout=timeout)
        return client

    CODE_MAP = {
        'ORCL': _oracle,
        'SSH': _ssh,
    }

    @classmethod
    def create(cls, guid):
        code, host, port, database_or_none, user, pswd = guid
        connect = cls.CODE_MAP.get(code, None)
        if connect is not None:
            try:
                return connect(host, port, database_or_none, user, pswd, timeout=cls.TIME_OUT)
            except (cx_Oracle.Error,) as e:
                log.warning('error has occurred while connect to %s: %s' %
                            (guid, e))
                raise DBConnectionError()
            except paramiko.SSHException as e:
                log.warning('error has occurred while connect to %s: %s' %
                            (guid, e))
                raise SSHConnectionError()
            except Exception as e:
                log.warning('error has occurred while connect to %s: %s' %
                            (guid, e))
                raise
        else:
            raise DBUnSupportedError()


class Reaper(object):
    def __init__(self, pool, interval=60):
        self._pool = pool
        self._delay = interval

    def _on_timer(self):
        try:
            self._pool.cleanup()
        except Exception as e:
            log.error('error has occurred while clean up pool: %s' % e)
        self._set_timer()

    def _set_timer(self):
        self._timer = threading.Timer(self._delay, self._on_timer)
        self._timer.daemon = True
        self._timer.start()

    def run(self):
        self._set_timer()


def makePath(sftp, target):
    # 切换根目录
    sftp.chdir('/')

    # 分割目标目录为目录单元集合
    data = target.split('/')
    # 进入目标目录, 目录不存在则创建
    for item in data:
        try:
            sftp.chdir(item)
        except:
            sftp.mkdir(item)
            sftp.chdir(item)


class Member(object):
    def __init__(self, group, guid, max_lifetime=1800):
        self._conn = None
        self._alive = False
        self._lifetime = time.time()
        self.group = group
        self.guid = guid
        self.max_lifetime = max_lifetime

    def is_expired(self):
        if time.time() - self._lifetime > self.max_lifetime:
            return True
        else:
            return False

    def connect(self):
        self._lifetime = time.time()
        if not self._alive:
            try:
                self._conn = ConnectionFactory.create(self.guid)
                self._alive = True
                log.debug('connect to %s success' % (self.guid,))
            except Exception:
                raise

    def stat(self, remote_dir):
        if self.guid[0] == 'ORCL':
            return True
        try:
            sftp = self._conn.open_sftp()
            return sftp.stat(remote_dir).st_atime
        except Exception as e:
            log.error('error has occurred while stat dir or file: %s' % e)
            return False
        finally:
            pass

    def upload(self, local_dir, remote_dir):
        if self.guid[0] == 'ORCL':
            return True
        try:
            sftp = self._conn.open_sftp()
            for root, dirs, files in os.walk(local_dir):
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    a = local_file.replace(local_dir, '').replace('/', '')
                    remote_file = os.path.join(remote_dir, a)
                    try:
                        sftp.put(local_file, remote_file)
                    except Exception as e:
                        makePath(sftp, os.path.split(remote_file)[0])
                        sftp.put(local_file, remote_file)
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(local_dir, '').replace('/', '')
                    remote_path = os.path.join(remote_dir, a)
                    try:
                        makePath(sftp, remote_path)
                    except Exception as e:
                        return False
            self._conn.exec_command("chmod a+rx -R %s" % remote_dir)
        except Exception as e:
            log.error('error has occurred while upload file: %s' % e)
            return False
        return True

    def get_fetch_result(self, cursor_or_v):
        if not isinstance(cursor_or_v, cx_Oracle.Cursor):
            return cursor_or_v
        try:
            result = []
            while (True):
                row = cursor_or_v.fetchone()
                if not row:
                    break
                tmp = []
                for i in row:
                    if isinstance(i, datetime.datetime):
                        i = i.strftime('%Y-%m-%d %H:%M:%S')
                    tmp.append(i)
                result.append(tmp)
            return result
        finally:
            try:
                cursor_or_v.close()
            except Exception:
                pass

    def call_procedure(self, name, **kwargs):

        """

        :param name: procedure name, exp. package.procedure
        :param in_args: []
        :param out_args: [],cx_Oracle Objects, ex->[cx_Oracle.CURSOR, cx_Oracle.STRING]
        :return: list of in_args and out_args
        :raise DBExecutionError: just a name
        """
        try:
            in_args = kwargs.pop('in_args', [])
            out_args = kwargs.pop('out_args', [])
            cursor = self._conn.cursor()
            out_args_parser = [cursor.var(i) for i in out_args]
            try:
                ret_cur = cursor.callproc(name, in_args + out_args_parser)
                return list(map(self.get_fetch_result, ret_cur))[len(in_args):]
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass
        except (cx_Oracle.InterfaceError, cx_Oracle.OperationalError):
            log.error('call procedure %s on %s with error' % (name, self.guid,))
            self._alive = False
            raise DBExecutionError()
        except cx_Oracle.DatabaseError as e:
            log.error('call procedure %s on %s with error: %s' % (name, self.guid, e))
            raise DBExecutionError()
        except Exception as e:
            log.error('call procedure %s on %s with other error: %s' % (name, self.guid, e))
            raise DBExecutionError()

    def execute(self, script, args):
        self._lifetime = time.time()
        if self.guid[0] == 'ORCL':
            return self.execute_sql(script, args)
        else:
            return self.execute_shell(script, args)

    def execute_shell(self, script, args):
        try:
            _, stdout, stderr = self._conn.exec_command(script + ' ' + ' '.join(args), timeout=100)
            errstr = stderr.readlines()
            result = stdout.readlines()
            channel = stdout.channel
            status = channel.recv_exit_status()
            if status:
                raise SSHScriptExecutionError(errstr)
            return result
        except SSHScriptExecutionError as e:
            log.error('execute on %s with script error: %s' % (self.guid, e))
            raise SSHExecutionError(e)
        except Exception as e:
            log.error('execute on %s with other error: %s' % (self.guid, e))
            self._alive = False
            raise SSHExecutionError(e)

    def execute_sql(self, sql, args, nset=1):
        try:
            cursor = self._conn.cursor()
            try:
                cursor.execute(sql, args)
                result = []
                while (True):
                    row = cursor.fetchone()
                    if not row:
                        break
                    tmp = []
                    for i in row:
                        if isinstance(i, datetime.datetime):
                            i = i.strftime('%Y-%m-%d %H:%M:%S')
                        tmp.append(i)
                    result.append(tmp)
                return result
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass
        # we assume InterfaceError and OperationalError as connection error
        # on these situations need reconnect next time
        except (cx_Oracle.InterfaceError, cx_Oracle.OperationalError,):
            log.error('execute on %s with connection error' % (self.guid,))
            self._alive = False
            raise DBExecutionError()
        except Exception as e:
            log.error('execute on %s with other error: %s' % (self.guid, e))
            raise DBExecutionError()

    def close(self):
        try:
            # oracle conn has cancel method to cancel long running sql
            try:
                self._conn.cancel()
            except Exception:
                pass
            self._conn.close()
        except Exception:
            pass
        self._alive = False
        self._conn = None
        log.debug('close member connection %s' % (self.guid,))

    def cleanup(self):
        if self.is_expired():
            log.debug('member was expired %s' % (self.guid,))
            self.close()
            self.group.drop(self)
            self.group = None


class Group(object):
    def __init__(self, pool, guid, max_size=5):
        self._lock = threading.RLock()
        self._free = collections.deque()
        self._used = collections.deque()
        self.pool = pool
        self.guid = guid
        self.max_size = max_size

    # this is not a thread safe function
    @property
    def size(self):
        return len(self._free) + len(self._used)

    # this is not a thread safe function
    def is_empty(self):
        return self.size == 0

    def acquire(self):
        with self._lock:
            if len(self._free):
                member = self._free.pop()
                self._used.appendleft(member)
                log.debug('find free member in %s' % (self.guid,))
            elif self.size < self.max_size:
                member = Member(self, self.guid)
                self._used.appendleft(member)
                log.debug('add new member into %s' % (self.guid,))
            else:
                log.warning('group %s was exhausted' % (self.guid,))
                raise GroupExhaustedError()
        return member

    def release(self, member):
        with self._lock:
            if member in self._used:
                self._used.remove(member)
                self._free.appendleft(member)
                log.debug('release member from %s' % (self.guid,))
            # maybe this is impossible :)
            else:
                log.error('release a ghost member from %s' % (self.guid,))

    def drop(self, member):
        with self._lock:
            if member in self._free:
                self._free.remove(member)
                log.debug('free up member from %s' % (self.guid,))
            # when free up a used memeber, and this member is pending
            # the db connection can not be freed up and cause connection leak
            elif member in self._used:
                log.error('cannt free up used member from %s' % (self.guid,))
            # maybe this is impossible :)
            else:
                log.error('cannt free up ghost member from %s' % (self.guid,))

    def cleanup(self):
        with self._lock:
            log.debug('total number of %d members in %s' %
                      (self.size, self.guid))
            # clean up all expired member in free queue
            # all members in used queue will keep going
            for member in list(self._free):
                member.cleanup()
            # group can only be deleted if it is empty
            # this is a passive method to free group
            if self.is_empty():
                self._free = None
                self._used = None
                self.pool.drop(self.guid)


class Pool(object):
    def __init__(self, reaper=None):
        self._lock = threading.Lock()
        self._pool = dict()
        if not reaper:
            self._reaper = Reaper(self)
        else:
            self._reaper = reaper
        self._reaper.run()

    @contextlib.contextmanager
    def acquire(self, guid):
        with self._lock:
            if guid in self._pool:
                group = self._pool[guid]
                log.debug('find group %s in pool' % (guid,))
            else:
                group = Group(self, guid)
                self._pool[guid] = group
                log.debug('add new group %s into pool' % (guid,))
        try:
            member = None
            member = group.acquire()
            member.connect()
            yield member
        finally:
            if member:
                self.release(member)

    def release(self, member):
        group = member.group
        group.release(member)

    def drop(self, guid):
        with self._lock:
            del self._pool[guid]
            log.debug('free up group %s from pool' % (guid,))

    def cleanup(self):
        log.debug('total number of %d groups' % len(self._pool))
        pool = copy.copy(self._pool)
        for guid, group in pool.items():
            group.cleanup()
