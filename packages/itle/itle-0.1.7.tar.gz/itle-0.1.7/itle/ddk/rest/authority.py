# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi
from itle.ddk.ddk_channel_type import DDKChannelType2


class DDKPidAuthorityRequest(RestApi):
    """查询是否完成备案"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKPidAuthorityRequest, self).__init__(aio_http, domain, port, token)

        self.ddk_pid = None
        self.custom_params = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid_auth'

    def get_method(self):
        return "GET"


class DDKPidAuthorityUrlRequest(RestApi):
    """创建备案链接"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKPidAuthorityUrlRequest, self).__init__(aio_http, domain, port, token)
        self.user_id = None
        self.channel_type: [int] = DDKChannelType2.GENERATE_BIND_URL.value
        self.amount = None
        self.scratch_card_amount = None
        self.diy_one_yuan_param = None
        self.diy_red_packet_param = None
        self.generate_qq_app = None
        self.generate_we_app = None
        self.generate_schema_url = None
        self.generate_short_url = None

    def get_api_uri(self):
        return '/api/1.0/ddk/pid_auth'

    def get_method(self):
        return 'POST'
