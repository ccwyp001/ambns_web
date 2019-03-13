# -*- coding: utf-8 -*-


from .base import BaseDispatchApi


class DispatchMember(BaseDispatchApi):
    def on_duty(self, is_on_duty=0, org_id='', xzbm=''):
        return self._get(
            'GET_V_STAFF_ONDUTY',
            params={
                'sfsb': is_on_duty,
                'orgid': org_id,
                'xzbm': xzbm
            }
        )
