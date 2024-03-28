#!/usr/bin/env python3
"""
Using Redis NoSQL database
"""

import redis
import uuid
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    takes a single method Callable argument and returns a Callable
    """

    @wraps(method)
    def increment(self, *args, **kwargs) -> Any:
        """
        increments the count for that key every time the method is called
        and returns the value returned by the original method
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return increment

def call_history(method: Callable) -> Callable:
    """
    Tracks the call details of a method in a Cache class
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs and output.
        """
        init_key = '{}:inputs'.format(method.__qualname__)
        fin_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(init_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(fin_key, output)
        return output
    return invoker

def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class' method.
    """

    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)

    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))

class Cache:
    """
    Initializes an Object for data
    """

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        take a key string argument and an optional Callable argument named fn
        """

        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.
        """

        return self.get(key, lambda x: int(x))
