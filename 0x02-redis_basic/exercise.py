#!/usr/bin/env python3
"""exercise.py module defines a cache class and inits redis."""
from typing import Union
import redis
import uuid


class Cache():
    """Cache class."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, str, bytes, float]):
        """Store value into redis database."""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
