#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemethod.py
An abstract class which implements the basic structure for creating methods.
"""
# Package Header #
from .__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #
from functools import update_wrapper
from typing import Any, Callable, Optional, Union

# Third-Party Packages #

# Local Packages #
from .baseobject import BaseObject, search_sentinel


# Definitions #
# Classes #
class BaseMethod(BaseObject):
    """An abstract class which implements the basic structure for creating methods.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _instances: Copies of this object for specific owner instances.

    Args:
        func: The function to wrap.
        init: Determines if this object will construct.
    """
    sentinel = search_sentinel

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func: Optional[Callable] = None, init: Optional[bool] = True):
        # Special Attributes #
        self.__func__ = None
        self.__self__ = None

        # Attributes #
        self._get_method_ = self.get_self_bind
        self._instances = {}

        # Object Construction #
        if init:
            self.construct(func=func)

    @property
    def _get_method(self):
        """The method that will be used for the __get__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._get_method_

    @_get_method.setter
    def _get_method(self, value: Union[Callable, str]):
        self.set_get_method(value)

    # Descriptors
    def __get__(self, instance: Any, owner: Optional[Any] = None):
        """When this object is requested by another object as an attribute.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        return self._get_method_(instance, owner=owner)

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, func: Optional[Callable] = None):
        """The constructor for this object.

            Args:
                func:  The function to wrap.
            """
        if func is not None:
            self.__func__ = func
            update_wrapper(self, self.__func__)

    # Descriptor
    def set_get_method(self, method: Union[Callable, str]):
        """Sets the __get__ method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the __get__ method to.
        """
        if isinstance(method, str):
            method = getattr(self, method)

        self._get_method_ = method

    def get_self(self, instance: Any, owner: Optional[Any] = None) -> "BaseMethod":
        """The __get__ method where it returns itself.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        return self

    def get_self_bind(self, instance: Any, owner: Optional[Any] = None) -> "BaseMethod":
        """The __get__ method where it binds itself to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        if instance is not None and self.__self__ is not instance:
            self.bind(instance)
        return self

    def get_new_bind(self,
                     instance: Any,
                     owner: Optional[Any] = None,
                     new_binding: str = "get_self_bind") -> "BaseMethod":
        """The __get__ method where it binds a new copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the new object will use.
        """
        if instance is None:
            return self
        else:
            bound = self.bind_to_new(instance=instance)
            bound.set_get_method(new_binding)
            setattr(instance, self.__func__.__name__, bound)
            return bound

    def get_subinstance(self, instance: Any, owner: Optional[Any] = None) -> "BaseMethod":
        """The __get__ method where it binds a registered copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        if instance is None:
            return self
        else:
            bound = self._instances.get(instance, search_sentinel)
            if bound is search_sentinel:
                self._instances[instance] = bound = self.bind_to_new(instance=instance)
            return bound

    # Binding
    def bind(self, instance: Any, name: Optional[str] = None):
        """Binds this object to another object to give this object method functionality.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.
        """
        self.__self__ = instance
        if name is not None:
            setattr(instance, name, self)

    def bind_to_new(self, instance: Any, name: Optional[str] = None) -> Any:
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.

        Returns:
            The new bound deepcopy of this object.
        """
        new_obj = type(self)(func=self.__func__, collective=self._is_collective)
        new_obj.bind(instance, name=name)
        return new_obj
