# -*- coding: utf-8 -*-


class Error(Exception):
    pass


class DBUnSupportedError(Error):
    pass


class DBConnectionError(Error):
    pass


class SSHConnectionError(Error):
    pass


class SSHExecutionError(Error):
    pass

class SSHScriptExecutionError(Error):
    pass


class DBExecutionError(Error):
    pass


class GroupExhaustedError(Error):
    pass
