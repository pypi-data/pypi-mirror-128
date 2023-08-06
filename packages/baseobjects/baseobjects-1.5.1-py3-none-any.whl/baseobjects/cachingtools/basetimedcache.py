#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basetimedcache.py
An abstract class for creating timed cahce
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
import abc
from time import perf_counter

# Third-Party Packages #

# Local Packages #
from ..basemethod import BaseMethod
from ..baseobject import BaseObject


# Definitions #
# Classes #
class _HashedSeq(list):
    """A hash value based on an iterable.

    Attributes:
        hashvalue: The hash value to store.

    Args:
        tuple_: The iterable to create a hash value from.
        hash_: The function that will create hash value.
    """
    __slots__ = "hashvalue"

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, tuple_, hash_=hash):
        # Attributes #
        self[:] = tuple_
        self.hashvalue = hash_(tuple_)

    # Representation
    def __hash__(self):
        """Get the hash value of this object."""
        return self.hashvalue


class CacheItem(BaseObject):
    """An item within a cache which contains the result and a link to priority.

    Attributes:
        priority_link: The object that represents this item's priority.
        key: The key to this item in the cache.
        result: The cached value.

    Args:
        key: The key to this item in the cache.
        result: The value to store in the cache.
        priority_link: The object that represents this item's priority.
    """
    __slots__ = ["key", "result", "priority_link"]

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, key=None, result=None, priority_link=None):
        # Attributes #
        self.priority_link = priority_link

        self.key = key
        self.result = result


class BaseTimedCache(BaseMethod):
    """A cache wrapper object for a function which resets its cache periodically.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.
        cache_item_type = The class that will create the cache items.

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
    cache_item_type = CacheItem

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func=None, typed=False, lifetime=None, call_method="cache_call", collective=True,  init=True):
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._is_collective = True

        self.typed = False
        self.is_timed = True
        self.lifetime = None
        self.expiration = None

        self.cache = None
        self._defualt_caching_method = self.no_cache
        self._caching_method = self.no_cache

        self._call_method = None

        # Object Construction #
        if init:
            self.construct(func=func, lifetime=lifetime, typed=typed, call_method=call_method, collective=collective)

    @property
    def is_collective(self):
        """Determines if the cache is collective for all method bindings or for each instance.

        When set, the __get__ method will be changed to match the chosen style.
        """
        return self._is_collective

    @is_collective.setter
    def is_collective(self, value):
        if value is True:
            self._get_method_ = self.get_self_bind
        else:
            self._get_method_ = self.get_new_bind
        self._is_collective = value

    @property
    def caching_method(self):
        """The method that will be used for caching.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._caching_method

    @caching_method.setter
    def caching_method(self, value):
        self.set_caching_method(value)

    @property
    def call_method(self):
        """The method that will be used for the __call__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._call_method

    @call_method.setter
    def call_method(self, value):
        self.set_call_method(value)

    # Callable
    def __call__(self, *args, **kwargs):
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.call_method(*args, **kwargs)

    # Instance Methods #
    # Constructors
    def construct(self, func=None, typed=None, lifetime=None,  call_method=None, collective=None):
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            collective: Determines if the cache is collective for all method bindings or for each instance.
        """
        if lifetime is not None:
            self.lifetime = lifetime
        self.expiration = perf_counter()

        if typed is not None:
            self.typed = typed

        if call_method is not None:
            self.set_call_method(call_method)

        if collective is not None:
            self.is_collective = collective

        super().construct(func=func)

    # Binding
    def get_new_bind(self, instance, owner=None, new_binding="get_self"):
        """The __get__ method where it binds a new copy to the other object. Changed the default parameter.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the new object will use.
        """
        return super().get_new_bind(instance, owner=owner, new_binding=new_binding)

    # Object Calling
    def set_call_method(self, method):
        """Sets the call method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the call method to.
        """
        if method is None:
            method = self.__func__
        elif isinstance(method, str):
            method = getattr(self, method)

        self._call_method = method

    def caching_call(self, *args, **kwargs):
        """Calls the caching function and clears the cache at certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        if self.clear_condition():
            self.clear_cache()

        return self.caching_method(*args, **kwargs)

    def clearing_call(self, *args, **kwargs):
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        self.clear_cache()

        return self.caching_method(*args, **kwargs)

    def clear_condition(self, *args, **kwargs):
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

    # Binding
    def bind_to_new(self, instance, name=None):
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.

        Returns:
            The new bound deepcopy of this object.
        """
        if hasattr(self, self._call_method.__name__):
            call_method = self._call_method.__name__
        else:
            call_method = self._call_method

        new_obj = type(self)(func=self.__func__, typed=self.typed, lifetime=self.lifetime,
                             call_method=call_method, collective=self._is_collective)
        new_obj.bind(instance, name=name)
        return new_obj

    # Caching
    def create_key(self, args, kwds, typed, kwd_mark=(object(),), fasttypes={int, str},
                   tuple_=tuple, type_=type, len_=len):
        """Make a cache key from optionally typed positional and keyword arguments.

        The key is constructed in a way that is flat as possible rather than
        as a nested structure that would take more memory.

        If there is only a single argument and its data type is known to cache
        its hash value, then that argument is returned without a wrapper.  This
        saves space and improves lookup speed.

        """
        # All of code below relies on kwds preserving the order input by the user.
        # Formerly, we sorted() the kwds before looping.  The new way is *much*
        # faster; however, it means that f(x=1, y=2) will now be treated as a
        # distinct call from f(y=2, x=1) which will be cached separately.
        key = args
        if kwds:
            key += kwd_mark
            for item in kwds.items():
                key += item
        if typed:
            key += tuple_(type_(v) for v in args)
            if kwds:
                key += tuple_(type_(v) for v in kwds.values())
        elif len_(key) == 1 and type_(key[0]) in fasttypes:
            return key[0]
        return _HashedSeq(key)

    def no_cache(self, *args, **kwargs):
        """A direct call to wrapped function with no caching.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__func__(*args, **kwargs)

    def set_caching_method(self, method=None):
        """Sets the caching method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the caching method to.
        """
        if isinstance(method, str):
            method = getattr(self, method)
        elif methed is None:
            method = self._defualt_caching_method

        self._caching_method = method

    @abc.abstractmethod
    def clear_cache(self):
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime
