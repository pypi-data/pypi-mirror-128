#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedcache.py
A cache that periodically resets and include its instantiation decorator function.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from time import perf_counter

# Third-Party Packages #

# Local Packages #
from .basetimedcache import BaseTimedCache
from ..objects import CirularDoublyLinkedContainer


# Definitions #
# Classes #
class TimedCache(BaseTimedCache):
    """A cache wrapper object for a function which resets its cache periodically.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.
        cache_item_type = The class that will create the cache items.
        priority_queue_type = The type of priority queue to hold cache item priorities.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.
        _instances: Copies of this object for specific owner instances.

        _maxsize: The max size of the lru_cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        priority: A container that keeps track of cache deletion priority.
        cache: Contains the results of the wrapped function.
        _defualt_caching_method: The default caching function to use.
        _caching_method: The designated function to handle caching.

        _call_method: The function to call when this object is called.

    Args:
        func: The function to wrap.
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """
    priority_queue_type = CirularDoublyLinkedContainer

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func=None, maxsize=None, typed=False, lifetime=None,
                 call_method="cache_call", collective=True,  init=True):
        # Parent Attributes #
        super().__init__(init=False)

        self.cache = {}
        self._defualt_caching_method = self.unlimited_cache
        self._caching_method = self.unlimited_cache

        # New Attributes #
        self._maxsize = None

        self.priority = self.priority_queue_type()

        # Object Construction #
        if init:
            self.construct(func=func, lifetime=lifetime, maxsize=maxsize, typed=typed,
                           call_method=call_method, collective=collective)

    @property
    def maxsize(self):
        """The cache's max size and when updated it changes the cache to its optimal handle function."""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value):
        self.set_maxsize(value)

    # Container Methods
    def __len__(self):
        """The method that gets this object's length."""
        return self.get_length()

    # Instance Methods #
    # Constructors
    def construct(self, func=None, maxsize=None, typed=None, lifetime=None,  call_method=None, collective=None):
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            maxsize: The max size of the cache.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            collective: Determines if the cache is collective for all method bindings or for each instance.
        """
        if maxsize is not None:
            self.maxsize = maxsize

        super().construct(func=func, typed=typed, lifetime=lifetime, call_method=call_method, collective=collective)

    # Binding
    def bind_to_new(self, instance, name=None):
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.

        Returns:
            The new bound deepcopy of this object.
        """
        if self._call_method.__name__ in dir(self):
            call_method = self._call_method.__name__
        else:
            call_method = self._call_method

        new_obj = type(self)(func=self.__func__, maxsize=self.maxsize, typed=self.typed, lifetime=self.lifetime,
                             call_method=call_method, collective=self._is_collective)
        new_obj.bind(instance, name=name)
        return new_obj

    # Caching
    def set_maxsize(self, value):
        """Change the cache's max size to a new value and updates the cache to its optimal handle function.

        Args:
            value: The new max size of the cache.
        """
        if value is None:
            self.caching_method = self.unlimited_cache
        elif value == 0:
            self.caching_method = self.no_cache
        else:
            self.caching_method = self.limited_cache

        self._maxsize = value

    def poll(self):
        """Check if the cache has reached its max size."""
        return self.cache.__len__() <= self._maxsize

    def get_length(self):
        """Gets the length of the cache."""
        return self.cache.__len__()

    def unlimited_cache(self, *args, **kwargs):
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_item = self.cache.get(key, self.sentinel)

        if cache_item is not self.sentinel:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            self.cache[key] = self.cache_item_type(key=key, result=result)
            return result

    def limited_cache(self, *args, **kwargs):
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_item = self.cache.get(key, self.sentinel)

        if cache_item is not self.sentinel:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            if self.cache.__len__() <= self._maxsize:
                self.cache[key] = self.cache_item_type(result=result)
            return result

    def clear_cache(self):
        """Clear the cache and update the expiration of the cache."""
        self.cache.clear()
        self.priority.clear()
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


# Functions #
def timed_cache(maxsize=None, typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed cache function factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed cache function factory.
    """

    def timed_cache_factory(func):
        """A factory for wrapping a function with a TimedCache object.

        Args:
            func: The function to wrap with a TimedCache.

        Returns:
            The TimeCache object which wraps the given function.
        """
        return TimedCache(func, maxsize=maxsize, typed=typed, lifetime=lifetime,
                          call_method=call_method, collective=collective)

    return timed_cache_factory
