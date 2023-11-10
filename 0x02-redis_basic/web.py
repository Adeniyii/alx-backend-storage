#!/usr/bin/env python3
"""module for request caching.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def cache_req(method: Callable) -> Callable:
    """Caches the output of fetched data."""

    @wraps(method)
    def inner(url) -> str:
        """The wrapper function for caching the output."""
        count_key = "count:{}".format(url)
        result_key = "result:{}".format(url)
        redis_store.expire(count_key, 10)
        result = redis_store.get(result_key)
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(result_key, result, ex=10)
        redis_store.incr(count_key)
        return result

    return inner


@cache_req
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the response."""
    return requests.get(url).text
