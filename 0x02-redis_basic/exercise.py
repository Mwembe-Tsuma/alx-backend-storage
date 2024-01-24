#!/usr/bin/env python3
""" Main file """

import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        # Initialize Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__

            count = self._redis.incr(key)

            result = method(self, *args, **kwargs)

            return result

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        # Get data from Redis
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data
