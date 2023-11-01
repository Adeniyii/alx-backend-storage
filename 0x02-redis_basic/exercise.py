#!/usr/bin/env python3
"""exercise.py module defines a cache class and inits redis."""
from typing import Callable, Optional, Union
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count_calls decorator to register no of calls to decorated func."""

    @wraps(method)
    def inner(self, data):
        key = method.__qualname__
        self._redis.incr(key)
        v = method(self, data)
        return v

    return inner


def call_history(method: Callable) -> Callable:
    """memoize function calls in redis db."""

    @wraps(method)
    def inner(self, *args):
        """inner function"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        out = method(self, *args)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(out))

        return out

    return inner


class Cache():
    """Cache class."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
