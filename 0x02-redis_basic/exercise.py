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


def replay(method: Callable):
    """replay cache history"""
    r = redis.Redis()
    base_key = method.__qualname__
    input_key = base_key + ":inputs"
    output_key = base_key + ":outputs"
    call_count = r.get(base_key)

    try:
        assert isinstance(call_count, bytes)
        call_count = call_count.decode("utf-8")
    except Exception:
        call_count = 0

    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(base_key, call_count))

    zipped = zip([i.decode("utf-8") for i in inputs],
                 [o.decode("utf-8") for o in outputs])
    for tup in list(zipped):
        t1 = tup[0]
        v1 = tup[1]

        print("{}(*{}) -> {}".format(base_key, t1, v1))


class Cache():
    """Cache class."""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store value into redis database."""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
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

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(
        "{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange(
        "{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
    replay(cache.store)
