# -*- coding: utf-8 -*-

from .base import BaseDispatchClient
from . import api


class DispatchClient(BaseDispatchClient):
    API_BASE_URL = 'http://172.30.1.102:8888/ZIT_WebService.asmx/'

    member = api.DispatchMember()

    def __init__(self, timeout=None):
        super(DispatchClient, self).__init__(
            timeout
        )
