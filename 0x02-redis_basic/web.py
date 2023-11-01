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

        r.incr(f"count:{url}")
        cached_html = r.get(url)
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        c_key = "result:{}".format(url)
        r.set(c_key, ex=10, value=html)
        return html

    return inner


@cache_req
def get_page(url: str) -> str:
    """ Inside get_page track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an expiration time
    of 10 seconds. """
    return requests.get(url).text
