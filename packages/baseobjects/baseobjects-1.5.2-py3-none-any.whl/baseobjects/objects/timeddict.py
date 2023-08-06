#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timeddict.py
A dictionary taht clears its contents after a specified time has passed.
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
from collections import UserDict
from contextlib import contextmanager
from time import perf_counter

# Third-Party Packages #

# Local Packages #
from baseobjects import BaseObject

# Definitions #
# Classes #
class TimedDict(UserDict):
    """A dictionary that clears its contents after a time has eplapsed.

    Attributes:
        is_timed: Determines if the dictionary will be reset periodically.
        lifetime: The period between dictionary resets in seconds.
        expiration: The next time the dictionary will be rest.

    Args:
        dict: The dictrionary to copy into this dictionary.
        **kwargs: The key words to add to this dictionary.
    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict=None, /, **kwargs):
        self.is_timed = True
        self.lifetime = None
        self.expiration = None

        self._data = {}
        if dict is not None:
            self.update(dict)
        if kwargs:
            self.update(kwargs)

    @property
    def data(self):
        """The data of the dictionary, """
        self.verify()
        return self._data

    # Instance Methods #
    # Mapping
    def clear(self):
        """Clears the contents of the dictionary and resets the expiration."""
        self._data.clear()
        self.reset_expiration()

    # Time Verification
    def reset_expiration(self):
        """Updates the expiration to a new future time."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    @contextmanager
    def pause_timer(self):
        """A context manager that will stop clearing the dictionary until it is returned."""
        left_over = 0
        if expiration is not None:
            left_over = self.expiration - perf_counter()
            self.expiration = None
        self.is_timed = False
        yield
        self.expiration = perf_counter() + left_over
        self.is_timed = True


    @contextmanager
    def pause_reset_timer(self):
        """A context manager that will stop clearing the dictionary until it is returned, resting the expiration."""
        self.is_timed = False
        yield
        self.is_timed = True
        self.reset_expiration()

    def clear_condition(self, *args, **kwargs):
        """The condition used to determine if the dictionary should be cleared.

        Args:
            *args: Arguments that could be used to determine if the dictionary should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the dictionary should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

    def verify(self):
        """Verifies if the dictionary should be cleared and then clears it."""
        if self.clear_condition():
            self.clear()

