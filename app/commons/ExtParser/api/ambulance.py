# -*- coding: utf-8 -*-

from .base import BaseDispatchApi


class DispatchAmbulance(BaseDispatchApi):
    def ambulance_info(self, xzbm=''):
        return self._get(
            'Get_All_CLLB_INFO',
            params={
                'xzbm': xzbm
            }
        )
