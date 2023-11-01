#!/usr/bin/env python3
"""Implements simple caching for http requests."""
from functools import wraps
from typing import Callable
import redis
import requests


def cache_req(method: Callable) -> Callable:
    """caching decorator."""
    r = redis.Redis()
    r.flushdb()

    @wraps(method)
    def inner(*args: str):
        """inner function"""
        url = args[0]
        key = "count:{}".format(url)

        result = r.get("result:{}".format(url))
        if result:
            return result.decode("utf-8")

        res = method(*args)
        r.set("result:{}".format(key), res)
        r.incr(key)
        r.expire(key, 10)

        return res

    return inner


@cache_req
def get_page(url: str) -> str:
    """ Inside get_page track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an expiration time
    of 10 seconds. """
    r = requests.get(url)
    return r.text
