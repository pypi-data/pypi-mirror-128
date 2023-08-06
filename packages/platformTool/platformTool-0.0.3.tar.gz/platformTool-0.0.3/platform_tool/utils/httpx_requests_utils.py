#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/11/19 17:33
    Desc  :     RequestUtils-POST/GET
--------------------------------------
"""
import httpx
from httpx import Response, AsyncClient
from loguru import logger

TIME_OUT = 899999


class RequestUtils:
    """封装Httpx请求"""

    def __init__(self, isHeaders):
        self.path: str = ''
        self.url: str = ''
        self.headers: dict = {}
        self.isHeaders: bool = isHeaders

    def result(self):
        return None


class PostRequestUtils(RequestUtils):
    """封装的POST请求"""

    def __init__(self, isHeaders):
        super().__init__(isHeaders)
        self.body = None

    @logger.catch
    def result(self) -> Response:
        logger.info(f'请求:{self.__dict__}')
        res = httpx.post(url = self.path if self.path.strip()[:4] == 'http' else self.url + self.path, json = self.body,
                         headers = self.headers if self.isHeaders else None, timeout = TIME_OUT)
        logger.info(f'响应:{res.text}')
        logger.info(f'耗时:{res.elapsed}')
        return res


class GetRequestUtils(RequestUtils):
    """封装GET请求"""

    def __init__(self, isHeaders):
        super().__init__(isHeaders)
        self.params = None

    @logger.catch
    def result(self) -> Response:
        logger.info(f'请求:{self.__dict__}')
        res = httpx.get(url = self.path if self.path.strip()[:4] == 'http' else self.url + self.path,
                        params = self.params, headers = self.headers if self.isHeaders else None, timeout = TIME_OUT)
        logger.info(f'响应:{res.text}')
        logger.info(f'耗时:{res.elapsed}')
        return res


class AsyncPostRequestUtils(RequestUtils):
    """封装的异步POST请求"""

    def __init__(self, isHeaders):
        super().__init__(isHeaders)
        self.body = None

    @logger.catch
    async def result(self, client: AsyncClient) -> Response:
        logger.info(f'请求:{self.__dict__}')
        res = await client.post(url = self.path if self.path.strip()[:4] == 'http' else self.url + self.path,
                                json = self.body, headers = self.headers if self.isHeaders else None,
                                timeout = TIME_OUT)
        logger.info(f'响应:{res.text}')
        return res


class AsyncGetRequestUtils(RequestUtils):
    """封装的异步POST请求"""

    def __init__(self, isHeaders: bool = False):
        super().__init__(isHeaders)
        self.body = None

    @logger.catch
    async def result(self, client: AsyncClient) -> Response:
        logger.info(f'请求:{self.__dict__}')
        res = await client.get(url = self.path if self.path.strip()[:4] == 'http' else self.url + self.path,
                               params = self.body, headers = self.headers if self.isHeaders else None,
                               timeout = TIME_OUT)
        logger.info(f'响应:{res.text}')
        return res


class UploadFileRequestUtils(RequestUtils):
    """封装的POST请求上传文件"""

    def __init__(self, isHeaders):
        super().__init__(isHeaders)
        self.body = None

    @logger.catch
    def result(self, files: str) -> Response:
        logger.info(f'请求:{self.__dict__}')
        res = httpx.post(url = self.path if self.path.strip()[:4] == 'http' else self.url + self.path,
                         files = {'file': open(fr'{files}', 'rb')}, headers = self.headers if self.isHeaders else None,
                         timeout = TIME_OUT)
        logger.info(f'响应:{res.text}')
        logger.info(f'耗时:{res.elapsed}')
        return res
