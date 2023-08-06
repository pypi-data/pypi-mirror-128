#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedsinglecache.py
A timed cache that only hold a single item.
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


# Definitions #
# Classes #
class TimedSingleCache(BaseTimedCache):
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

        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        cache: Contains the results of the wrapped function.
        _defualt_caching_method: The default caching function to use.
        _caching_method: The designated function to handle caching.

        _call_method: The function to call when this object is called.

    Args:
        func: The function to wrap.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func=None, typed=False, lifetime=None, call_method="cache_call", collective=True,  init=True):
        # Parent Attributes #
        super().__init__(init=False)

        self._defualt_caching_method = self.caching
        self._caching_method = self.caching

        # New Attributes #
        self.args_key = None

        # Object Construction #
        if init:
            self.construct(func=func, lifetime=lifetime, typed=typed, call_method=call_method, collective=collective)

    # Instance Methods #
    # Caching
    def caching(self, *args, **kwargs):
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        if key != self.args_key:
            self.cache = self.__func__(*args, **kwargs)
            self.args_key = key

        return self.cache

    def clear_cache(self):
        """Clear the cache and update the expiration of the cache."""
        self.cache = None
        self.args_key = None
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


# Functions #
def timed_single_cache(typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed single cache function factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed single cache function factory.
    """

    def timed_single_cache_factory(func):
        """A factory for wrapping a function with a TimedSingleCache object.

        Args:
            func: The function to wrap with a TimedSingleCache.

        Returns:
            The TimeSingleCache object which wraps the given function.
        """
        return TimedSingleCache(func, typed=typed, lifetime=lifetime, call_method=call_method, collective=collective)

    return timed_single_cache_factory
