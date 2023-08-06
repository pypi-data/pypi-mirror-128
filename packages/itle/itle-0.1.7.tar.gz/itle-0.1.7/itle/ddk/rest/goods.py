# -*- coding: UTF-8 -*-
import aiohttp as aiohttp

from itle.base import RestApi


class DDKSearchGoodsRequest(RestApi):
    """商品搜索请求"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKSearchGoodsRequest, self).__init__(aio_http, domain, port, token)
        # self.ddk_pid = None
        # self.custom_params = None
        self.user_id = None
        self.activity_tags = None
        self.ddk_cat_id = None
        self.goods_sign_list = None
        self.is_brand_goods = None
        self.keyword = None
        self.list_id = None
        self.merchant_type = None
        self.merchant_type_list = None
        self.opt_id = None
        self.with_coupon = None
        self.use_customized = None
        self.range_list = None
        self.page_index = None
        self.page_size = None
        self.ddk_sort_type = None

    def get_api_uri(self):
        return '/api/1.0/ddk/search_goods_list'

    def get_method(self):
        return 'GET'


class DDKTopGoodsRequest(RestApi):
    """top goods 请求"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKTopGoodsRequest, self).__init__(aio_http, domain, port, token)
        # self.ddk_pid = None
        self.offset = None
        self.limit = None
        self.list_id = None
        self.ddk_sort_type = None

    def get_api_uri(self):
        return '/api/1.0/ddk/top_goods_list'

    def get_method(self):
        return 'GET'


class DDKRecommendGoodsRequest(RestApi):
    """推荐商品请求"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKRecommendGoodsRequest, self).__init__(aio_http, domain, port, token)
        # self.ddk_pid = None
        # self.custom_params = None
        self.user_id = None
        self.offset = None
        self.limit = None
        self.channel_type = None
        self.list_id = None
        self.goods_sign_list = None
        self.activity_tags = None
        self.cat_id = None

    def get_api_uri(self):
        return '/api/1.0/ddk/recommend_goods_list'

    def get_method(self):
        return 'GET'


class DDKGoodsDetailsRequest(RestApi):
    """获取商品详情"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKGoodsDetailsRequest, self).__init__(aio_http, domain, port, token)

        self.goods_sign = None
        self.search_id = None
        self.goods_id = None

    def get_api_uri(self):
        return f'/api/1.0/ddk/goods/{self.goods_id}'

    def get_method(self):
        return 'GET'


class DDKGoodsPromUrlRequest(RestApi):
    """生成商品推广链接"""

    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str):
        super(DDKGoodsPromUrlRequest, self).__init__(aio_http, domain, port, token)
        self.user_id = None
        self.search_id = None
        self.goods_sign = None
        self.goods_id_list = None
        self.generate_authority_url = None
        self.generate_mall_collect_coupon = None
        self.generate_schema_url = None
        self.generate_short_url = None
        self.generate_qq_app = None
        self.generate_we_app = None
        self.material_id = None
        self.multi_group = None

    def get_api_uri(self):
        return '/api/1.0/ddk/goods_prom_url'

    def get_method(self):
        return 'GET'
