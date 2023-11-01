#!/usr/bin/env python3
"""Implements simple caching for http requests."""
from functools import wraps
from typing import Callable
import redis
import requests


r = redis.Redis()


def cache_req(method: Callable) -> Callable:
    """caching decorator."""

    @wraps(method)
    def inner(url: str) -> str:
        """inner function"""
        key = "result:{}".format(url)

        result = r.get(key)
        if result:
            return result.decode("utf-8")

        res = method(url)
        r.set(key, res)
        r.incr("count:{}".format(url))
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
