#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" automaticproperties.py
An abstract class which creates properties for this class automatically.
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
from abc import abstractmethod
from builtins import property
from typing import Any, Callable, Iterable, Optional

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject
from .initmeta import InitMeta


# Definitions #
# Classes #
class AutomaticProperties(BaseObject, metaclass=InitMeta):
    """An abstract class which creates properties for this class automatically.

    Class Attributes:
        _properties_map (list): A list of names and functions used to create properties.
    """
    _properties_map = []

    # Class Methods #
    # Class Construction
    @classmethod
    def _init_class_(cls):
        """A method that runs after class creation, creating the properties for this class."""
        cls._construct_properties_map()
        cls._construct_properties()

    # Callbacks
    @classmethod
    def _get(cls, obj: Any, name: str) -> Any:
        """A generic get which can be implemented in a subclass.

        Args:
            obj: The target object to get the attribute from.
            name: The name of the attribute to get from the object.

        Returns:
            The item to return.
        """
        getattr(obj, name)

    @classmethod
    def _set(cls, obj: Any, name: str, value: Any):
        """A generic set which can be implemented in a subclass.

        Args:
            obj: The target object to set.
            name: The name of the attribute to set.
            value: The the item to set within the target object.
        """
        setattr(obj, name, value)

    @classmethod
    def _del(cls, obj: Any, name: str):
        """A generic delete which can be implemented in a subclass.

        Args:
            obj (Any): The target object to delete an attribute from.
            name (str): The name of attribute to delete in the object.
        """
        delattr(obj, name)

    # Callback Factories
    @classmethod
    def _default_callback_factory(cls, info: Any):
        """An example factory for creating property modification functions.

        Args:
            info (Any): An object that can be use to create the get, set, and delete functions

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        name = info

        def get_(obj):
            """Gets the object."""
            return cls._get(obj, name)

        def set_(obj, value):
            """Sets the wrapped object."""
            cls._set(obj, name, value)

        def del_(obj):
            """Deletes the wrapped object."""
            cls._del(obj, name)

        return get_, set_, del_

    # Property Constructors
    @classmethod
    def _iterable_to_properties(cls, iter_: Iterable, callback_factory: Callable):
        """Create properties for this class based on an iterable where the items are the property names.

        Args:
            iter_: The names of the properties which the factories will use to create functions.
            callback_factory: The factory that creates get, set, del, functions for the property.
        """
        for name in iter_:
            if not hasattr(cls, name):
                get_, set_, del_ = callback_factory(name)
                setattr(cls, name, property(get_, set_, del_))

    @classmethod
    def _dictionary_to_properties(cls, dict_: dict, callback_factory: Callable):
        """Create properties for this class based on a dictionary where the keys are the property names.

        Args:
            dict_: The names of the properties and some info to help the factory create functions.
            callback_factory: The factory that creates get, set, del, functions for the property.
        """
        for name, info in dict_.items():
            if not hasattr(cls, name):
                get_, set_, del_ = callback_factory(info)
                setattr(cls, name, property(get_, set_, del_))

    # Properties Mapping
    @classmethod
    @abstractmethod
    def _construct_properties_map(cls):
        """An abstract method that assigns how properties should be constructed."""
        # cls._properties_map.append(["name", cls._dictionary_to_properties, cls._default_callback_factory])
        pass

    # Properties Constructor
    @classmethod
    def _construct_properties(cls, map_: Optional[list] = None):
        """Constructs all properties from a list which maps the properties and their functionality.

        Args:
            map_: A list to map the properties from.
        """
        if map_ is not None:
            cls._properties_map = map_

        for map_name, constructor, factory in cls._properties_map:
            try:
                constructor(getattr(cls, map_name), factory)
            except AttributeError:
                raise AttributeError("An attribute is missing")
