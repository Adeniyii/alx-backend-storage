#!/usr/bin/env python3
"""exercise.py module defines a cache class and inits redis."""
from typing import Callable, Optional, Union
import redis
import uuid
from functools import wraps


def count_calls(func: Callable) -> Callable:
    """count_calls decorator to register no of calls to decorated func."""

    @wraps(func)
    def inner(self, data):
        key = func.__qualname__
        vv = self.get_int(key)
        self._redis.set(key, vv + 1)
        v = func(self, data)
        return v

    return inner


class Cache():
    """Cache class."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[int, str, bytes, float]) -> str:
        """Store value into redis database."""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[bytes, int, str, float, None]:
        """Get and convert value from redis db."""
        v = self._redis.get(key)
        if fn is not None:
            return fn(v)
        return v

    def get_str(self, key: str) -> str:
        '''Retrieves string value from Redis db.
        '''
        v = self.get(key, str)
        assert isinstance(v, str)
        return v

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.
        '''
        v = self.get(key, lambda x: int(x) if x else 0)
        assert isinstance(v, int)
        return v


if __name__ == "__main__":
    cache = Cache()

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))
