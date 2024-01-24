#!/usr/bin/env python3
""" Writing strings to Redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__

            count = self._redis.incr(key)

            result = method(self, *args, **kwargs)

            print(f"Method '{key}' called {count} times")

            return result

        return wrapper

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        # Convenience method for getting a string
        return self.get(key, fn=lambda d: d.decode("utf-8")
                        if isinstance(d, bytes) else d)

    def get_int(self, key: str) -> Union[int, None]:
        # Convenience method for getting an integer
        return self.get(key, fn=int)