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
        redis_store.incr(f"count:{url}")
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f"result:{url}", result, ex=10)
        return result

    return inner


@cache_req
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the response."""
    return requests.get(url).text
