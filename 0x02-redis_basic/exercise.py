#!/usr/bin/env python3
"""exercise.py module defines a cache class and inits redis."""
from typing import Any, Callable, Union
import redis
import uuid


class Cache():
    """Cache class."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, str, bytes, float]) -> str:
        """Store value into redis database."""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable[[Union[bytes, None]], Any]):
        """Get and convert value from redis db."""
        v = self._redis.get(key)
        if fn is not None:
            return fn(v)
        return v


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
