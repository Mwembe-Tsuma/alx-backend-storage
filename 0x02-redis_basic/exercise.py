#!/usr/bin/env python3
""" Writing strings to Redis"""


import redis
import uuid
from typing import Any, Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator for Cache class methods"""
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ Wraps called method and adds its call count"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator for storing history of inputs and outputs"""
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> Any:
        """Wraps called method to store inputs and outputs"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls for a particular function"""
    clients = redis.Redis()
    calls = clients.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              clients.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               clients.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialize new cache obj"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method"""
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Store method"""
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Convenience method for getting a string"""
        return self.get(key, fn=lambda d: d.decode("utf-8")
                        if isinstance(d, bytes) else d)

    def get_int(self, key: str) -> Union[int, None]:
        """Convenience method for getting an integer"""
        return self.get(key, fn=int)
