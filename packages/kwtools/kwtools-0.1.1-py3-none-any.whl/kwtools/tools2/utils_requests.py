import os
import sys
import re
import json
import traceback
import user_agent
import socket
import websocket
import ssl
import time
import random
import requests
import collections
import urllib
import aiohttp
import asyncio
import functools
from copy import deepcopy
from retry import retry
from urllib.parse import urlparse

from kwtools.settings import logger
from kwtools.tools2.utils_python import retry_func


# Coroutine lockers. e.g. {"locker_name": locker}
METHOD_LOCKERS = {}


def async_method_locker(name, wait=True, timeout=1):
    """ In order to share memory between any asynchronous coroutine methods, we should use locker to lock our method,
        so that we can avoid some un-prediction actions.

    Args:
        name: Locker name.
        wait: If waiting to be executed when the locker is locked? if True, waiting until to be executed, else return
            immediately (do not execute).
        timeout: Timeout time to be locked, default is 1s.

    NOTE:
        This decorator must to be used on `async method`.
    """
    assert isinstance(name, str)

    def decorating_function(method):
        global METHOD_LOCKERS
        locker = METHOD_LOCKERS.get(name)
        if not locker:
            locker = asyncio.Lock()
            METHOD_LOCKERS[name] = locker

        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            if not wait and locker.locked():
                return # QUESTION: 直接返回None会有问题吗?
            try:
                await locker.acquire()
                return await asyncio.wait_for(method(*args, **kwargs), timeout)
                # return await method(*args, **kwargs)
            finally:
                locker.release()
        return wrapper
    return decorating_function


class AsyncRequests(object):
    """ Asynchronous HTTP Request Client.
    """

    # Every domain name holds a connection session, for less system resource utilization and faster request speed.
    _SESSIONS = {}  # {"domain-name": session, ... }

    @classmethod
    async def ensure_aio_req(cls, retry_times=5, timeout=10, **kwargs):
        """ Retry asyncio request
        """
        i = 1
        while i <= retry_times:
            try:
                if i != 1:
                    logger.info("====================================================")
                    logger.info(f"[网络请求异常] 尝试第 {i} 次访问....")
                    logger.info("====================================================")
                    await asyncio.sleep(1)
                code, success, error = await cls.aio_req(timeout=timeout, **kwargs)
                logger.debug(f"code <{type(code)}>: {code}")
                if success:
                    logger.debug(f"success <{type(success)}>: {success}")
                    return code, success, None
                elif error:
                    logger.error(f"error <{type(error)}>: {error}")
                    raise Exception(f"[网页请求异常] (第 {i} 次请求时)")
            except:
                e = traceback.format_exc(limit=10)
                logger.error(f"[网页请求崩溃] url:{kwargs['url']}")
                logger.error(e)
            i += 1
        return '', None, e



    @classmethod
    async def aio_req(cls, method="GET", url="", params={}, data={}, headers={}, timeout=10, **kwargs):
        """ Create a HTTP request.

        Args:
            method: HTTP request method. `GET` / `POST` / `PUT` / `DELETE`
            url: Request url.
            params: HTTP query params.
            data: HTTP request body, dict format.
            headers: HTTP request header.
            timeout: HTTP request timeout(seconds), default is 10s.

            **kwargs:
                cookies: pass
                proxy: HTTP proxy. (no proxy need to pass None, not "")
                auth: pass
                allow_redirects: default is True;
                verify_ssl: pass

        Return:
            code: HTTP response code.
            success: HTTP response data. If something wrong, this field is None.
            error: If something wrong, this field will holding a Error information, otherwise it's None.

        Raises:
            HTTP request exceptions or response data parse exceptions. All the exceptions will be captured and return
            Error information.
        """
        session = cls._get_session(url)
        try:
            if method.upper() == "GET":
                response = await session.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
            elif method.upper() == "POST":
                response = await session.post(url, params=params, json=data, headers=headers, timeout=timeout, **kwargs)
            elif method.upper() == "PUT":
                response = await session.put(url, params=params, json=data, headers=headers, timeout=timeout, **kwargs)
            elif method.upper() == "DELETE":
                response = await session.delete(url, params=params, json=data, headers=headers, timeout=timeout, **kwargs)
            else:
                error = "http method error!"
                return None, None, error
            logger.debug(f"response: {response}")
            code = response.status
            text = await response.text()
        except:
            e = traceback.format_exc(limit=10)
            logger.info(f"e: {e}")
            logger.info(f"method: {method}")
            logger.info(f"url: {url}")
            logger.info(f"params: {params}")
            logger.info(f"data: {data}")
            logger.info(f"headers: {headers}")
            logger.info(f"timeout: {timeout}")
            logger.info(f"proxy: {kwargs.get('proxy')}")
            return None, None, e

        if code not in (200, 201, 202, 203, 204, 205, 206):
            logger.info(f"method: {method}")
            logger.info(f"url: {url}")
            logger.info(f"params: {params}")
            logger.info(f"data: {data}")
            logger.info(f"headers: {headers}")
            logger.info(f"code: {code}")
            logger.info(f"timeout: {timeout}")
            logger.info(f"proxy: {kwargs.get('proxy')}")
            logger.info(f"response: {response}")
            logger.info(f"resp.text(): {text}")
            return code, None, text
        else:
            try:
                result = await response.json()
            except:
                result = await response.text()
            return code, result, None

    @classmethod
    def _get_session(cls, url):
        """ Get the connection session for url's domain, if no session, create a new.

        Args:
            url: HTTP request url.

        Returns:
            session: HTTP request session.
        """
        parsed_url = urlparse(url)
        key = parsed_url.netloc or parsed_url.hostname
        if key not in cls._SESSIONS:
            session = aiohttp.ClientSession()
            cls._SESSIONS[key] = session
        return cls._SESSIONS[key]

    @classmethod
    @async_method_locker("AsyncRequests.close.locker", timeout=5)
    async def close(cls):
        for key in list(cls._SESSIONS.keys()):
            await cls._SESSIONS[key].close()
            del cls._SESSIONS[key]





class UtilsRequests():
    def  __init__(self):
        pass



utils_requests = UtilsRequests()





async def test_AsyncRequests():
    # # CASE1:
    # # url = 'https://explorer.roninchain.com/address/ronin:3a19d7a2ab8a42f4db502f5cfab0391916e311d7/tokentxns?ps=100&p=1' # 可以正常访问
    # url = "https://explorer.roninchain.com/token/ronin:c6344bc1604fcab1a5aad712d766796e2b7a70b9" # 目前无法正常访问 (返回code:500页面)
    # proxy = None
    # code, success, error  = await AsyncRequests.ensure_aio_req(retry_times=3, method="GET", url=url, proxy=proxy)
    # print(f"code:{code}")
    # print(f"success:{success}")
    # print(f"error:{error}")
    # await AsyncRequests.close() # 记得关闭session (否则会有报错)


    # # CASE2:
    # task_lst = []
    # proxy="http://127.0.0.1:7890"
    #
    # url = 'https://api.binance.com/api/v3/time'
    # coro = AsyncRequests.ensure_aio_req(retry_times=3, method="GET", url=url, proxy=proxy)
    # task_lst.append(coro)
    #
    # url = 'https://api.binance.com/api/v3/time'
    # coro = AsyncRequests.ensure_aio_req(retry_times=3, method="GET", url=url, proxy=proxy)
    # task_lst.append(coro)
    #
    # x = await asyncio.gather(*task_lst) # [(200, {'serverTime': 1636306335397}, None), (200, {'serverTime': 1636306335398}, None)]
    # print("==============================================")
    # print(f"x {type(x)} : {x}")
    # for x, y, z in x:
    #     print(x)
    #     print(y)
    #     print(z)
    # print("==============================================")
    # await AsyncRequests.close() # 一定要记得close




    # # CASE3:
    url = "https://explorer.roninchain.com/_next/data/lNQyeI8jVUhj9VU9VhQ-a/tx/0x2e7f3b06b0fffafde76584fdd5b4d20ae5edae1e196d7eec20dd000cdecf83a0.json"
    url = 'https://explorer.roninchain.com/address/ronin:3a19d7a2ab8a42f4db502f5cfab0391916e311d7/tokentxns?ps=100&p=1' # 可以正常访问
    url = "https://explorer.roninchain.com/_next/data/2NTrPf5Ptvob5eLzOX2y2/tx/0xac5b46fd556767543e705a31bade534c358442f22919ab1833326d7e196c10d2.json"
    url = "https://explorer.roninchain.com/_next/data/2NTrPf5Ptvob5eLzOX2y2/tx/0xf3a9debe3a56d1df6a412711aada4d7cd8c7be009a23aaa08a94a8b319de64b9.json"
    proxy = None
    code, success, error  = await AsyncRequests.ensure_aio_req(retry_times=3, method="GET", url=url, proxy=proxy)
    print(f"code:{code}")
    print(f"success:{success}")
    print(f"error:{error}")
    await AsyncRequests.close() # 记得关闭session (否则会有报错)



if __name__ == '__main__':
    asyncio.run(test_AsyncRequests())
    pass
