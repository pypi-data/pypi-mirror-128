#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
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

# Third-Party Packages #

# Local Packages #
from ..basemeta import BaseMeta


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name, bases=None, namespace=None):
        super().__init__(name, bases, namespace)
        cls._init_class_()
