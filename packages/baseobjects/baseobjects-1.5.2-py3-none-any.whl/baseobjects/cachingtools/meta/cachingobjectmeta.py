#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachingobjectmeta.py
Creates a registry for the caching objects with a class.
"""
# Package Header #
from ...__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #

# Third-Party Packages #

# Local Packages #
from ...basemeta import BaseMeta
from ..basetimedcache import BaseTimedCache


# Definitions #
# Classes #
class CachingObjectMeta(BaseMeta):
    """Automatically makes a set of all function that are Timed Caches in the class."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if hasattr(cls, "_caches_"):
            cls._caches_ = cls._caches_.copy()
        else:
            cls._caches_ = set()

        for name, cls_attribute in namespace.items():
            if isinstance(cls_attribute, BaseTimedCache):
                cls._caches_.add(name)
