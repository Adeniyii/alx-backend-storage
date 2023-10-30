#!/usr/bin/env python3
""""""
from typing import Union
import redis
import uuid


class Cache():
    """"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, str, bytes, float]):
        """"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
