# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi
from itle.ddk.ddk_channel_type import DDKChannelType3


class DDKCmsPromUrlRequest(RestApi):
    """生成商城-频道推广链接"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token):
        super(DDKCmsPromUrlRequest, self).__init__(aio_http, domain, port, token)
        self.user_id = None
        self.channel_type = DDKChannelType3.PC_SHOPPING.value
        self.keyword = None
        self.multi_group = None
        self.generate_mobile = None
        self.generate_schema_url = None
        self.generate_short_url = None
        self.generate_we_app = None

    def get_api_uri(self):
        return '/api/1.0/ddk/cms_prom_url'

    def get_method(self):
        return 'GET'
