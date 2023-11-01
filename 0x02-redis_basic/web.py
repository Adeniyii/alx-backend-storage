#!/usr/bin/env python3
"""Implements simple caching for http requests."""
from functools import wraps
from typing import Callable
import redis
import requests


def cache_req(method: Callable) -> Callable:
    """caching decorator."""

    @wraps(method)
    def inner(*args: str):
        """inner function"""
        r = redis.Redis()
        r.flushdb()

        res = method(*args)
        url = args[0]
        key = "count:{}".format(url)

        r.incr(key, res)
        r.expire(key, 10)

        return res

    return inner


def get_page(url: str) -> str:
    """ Inside get_page track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an expiration time
    of 10 seconds. """
    r = requests.get(url)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        pass

    return r.text
