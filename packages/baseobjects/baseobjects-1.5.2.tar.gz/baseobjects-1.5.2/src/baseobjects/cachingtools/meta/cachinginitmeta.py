#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachinginitmeta.py
A mixin metaclass that implements caching and init functionalities
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
from ...objects.initmeta import InitMeta
from .cachingobjectmeta import CachingObjectMeta

# Definitions #
# Classes #
class CachingInitMeta(InitMeta, CachingObjectMeta):
    """Automatically makes a set of all function that are Timed Caches in the class."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name, bases, namespace):
        CachingObjectMeta.__init__(cls, name, bases, namespace)
        InitMeta.__init__(cls, name, bases, namespace)
