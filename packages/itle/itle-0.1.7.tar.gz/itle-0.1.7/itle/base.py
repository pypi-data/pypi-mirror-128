# -*- coding: UTF-8 -*-
from enum import Enum
from typing import Dict, Iterable, Optional

import aiohttp


class Message(Enum):
    SUCCESS = 0  # 成功
    FAIL = -1  # 返回错误信息
    EXCEPTION = -2  # 异常和异常信息
    SESSION_EXPIRED = -3  # 会话过期
    TOKEN_EXPIRE = -4  # token过期失效
    REPEAT_LOGIN = -5  # 重复登录
    USER_NOT_TB_AUTHORIZATION = -6  # 没有淘宝授权
    UPDATE_VERSION = -7  # 版本太低，app需要更新


class Resp:
    def __init__(self, code: int, msg: str, data: Optional[Iterable]):
        self.code = code
        self.msg = msg
        self.data = data

    def to_resp(self):
        return {'code': self.code, 'msg': self.msg, 'data': self.data}

    @classmethod
    def create_resp(cls, code: int = Message.SUCCESS.value, msg: str = 'success',
                    data: Optional[Iterable] = None) -> Dict:
        return {'code': code, 'msg': msg, 'data': data}

    @classmethod
    def create_resp_by_message(cls, message: Message = Message.SUCCESS, data: Optional[Iterable] = None):
        return Resp.create_resp(message.value, message.name, data)

    @classmethod
    def create_err_resp(cls, code: int = Message.FAIL.value, msg: str = Message.FAIL.name,
                        data: Optional[Iterable] = None) -> Dict:
        return Resp.create_resp(code, msg, data)


class RestApi:
    def __init__(self, aio_http: aiohttp, domain: str, port: int, token: str, context: str = ''):
        self.__aio_http = aio_http
        self.__domain = domain
        self.__port = port
        self.__token = token
        self.__context = context

    async def get_response(self) -> Dict:
        method = self.get_method()
        if method in ['GET', 'DELETE', 'OPTIONS', 'HEAD']:
            return await self.do_get()
        elif method == 'POST':
            return await self.do_post()
        elif method == 'PUT':
            return await self.do_put()
        elif method == 'DELETE':
            return await self.do_delete()
        elif method == 'OPTIONS':
            return await self.do_option()
        elif method == 'HEAD':
            return await self.do_head()
        elif method == 'PATCH':
            return await self.do_patch()
        else:
            raise Exception('unknown http method')

    async def do_get(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.get(self.__blt_url(), params=params, headers=headers) as r:
            return await r.json()

    async def do_post(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.post(self.__blt_url(), data=params, headers=headers) as r:
            return await r.json()

    async def do_put(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.put(self.__blt_url(), data=params, headers=headers) as r:
            return r.json()

    async def do_delete(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.delete(self.__blt_url(), params=params, headers=headers) as r:
            return await r.json()

    async def do_option(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.options(self.__blt_url(), params=params, headers=headers) as r:
            return await r.json()

    async def do_head(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.head(self.__blt_url(), params=params, headers=headers) as r:
            return await r.json()

    async def do_patch(self):
        params = self.get_app_params()
        headers = {}
        headers.update(self.__blt_authorization())
        async with self.__aio_http.patch(self.__blt_url(), data=params, headers=headers) as r:
            return await r.json()

    def get_api_uri(self):
        """api请求uri,子类实现"""
        pass

    def get_method(self):
        """请求方法，子类实现"""
        pass

    def __blt_url(self):
        """构造请求url"""
        return f'{self.__domain}:{self.__port}{self.__context}{self.get_api_uri()}'

    def __blt_authorization(self):
        return {'Authorization': f'Bearer {self.__token}'} if self.__token else {}

    def get_app_params(self):
        app_params = {}
        for key, value in self.__dict__.items():
            if not key.startswith("__") \
                    and key not in self.get_multipart_params() \
                    and not key.startswith("_RestApi__") \
                    and value is not None:
                if key.startswith("_"):
                    app_params[key[1:]] = str(value) if isinstance(value, bool) else value
                else:
                    app_params[key] = str(value) if isinstance(value, bool) else value

        # 查询翻译字典来规避一些关键字属性
        translate_param = self.get_translate_params()
        for key, value in app_params.items():
            if key in translate_param:
                app_params[translate_param[key]] = app_params[key]
                del app_params[key]

        return app_params

    def get_multipart_params(self):
        return []

    def get_translate_params(self):
        return {}
