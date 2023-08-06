#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" circulardoublylinkedcontainer.py
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
import copy

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class LinkedNode(BaseObject):
    """A node in a circular doubly linked container.

    Attributes:
        previous: The previous node.
        next: The next node.
        data: The data contained within this node.

    Args:
        data: The data to contain within this node.
        previous: The previous node.
        next_: The next node.
    """
    __slots__ = ["previous", "next", "data"]

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, data=None, previous=None, next_=None, init=True):
        # Attributes #
        self.previous = self
        self.next = self

        self.data = None

        # Object Construction #
        if init:
            self.construct(data=data, previous=previous, next_=next_)

    # Instance Methods #
    # Constructors
    def construct(self, data=None, previous=None, next_=None):
        """Constructs this object.

        Args:
            data: The data to contain within this node.
            previous: The previous node.
            next_: The next node.
        """
        self.previous = previous
        self.next = next_

        self.data = data


class CirularDoublyLinkedContainer(BaseObject):
    """A container that used nodes which at are doubly linked to one another to store data.

    Attributes:
        first_node: The first linked node in this container.
    """
    __slots__ = "first_node"

    # Magic Methods #
    # Construction/Destruction
    def __init__(self):
        # Attributes #
        self.first_node = None

    @property
    def is_empty(self):
        """Determines if this container is empty."""
        return self.first_node is None

    @property
    def last_node(self):
        """The last node in this container."""
        return self.first_node.previous

    def __deepcopy__(self, memo=None, _nil=[]):
        """The deepcopy magic method

        Args:
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        new_obj = type(self)()
        if not self.is_empty:
            original_node = self.first_node
            new_obj.append(data=copy.deepcopy(original_node.data))
            while original_node.next is not self.first_node:
                new_obj.append(data=copy.deepcopy(original_node.data))
                original_node = original_node.next

        return new_obj

    # Container Methods
    def __len__(self):
        """The method that gets this object's length."""
        return self.get_length()

    def __getitem__(self, item):
        """The method that allows index retrievals of stored items.

        Args:
            item: The index of the item to get.
        """
        return self.get_item(item)

    # Bitwise Operators
    def __lshift__(self, other):
        """Shift the start of nodes to the left by an amount.

        Args:
            other: The number of nodes to shift to the left.
        """
        self.shift_left(other)

    def __rshift__(self, other):
        """Shift the start of nodes to the right by an amount.

        Args:
            other: The number of nodes to right to the left.
        """
        self.shift_right(other)

    # Instance Methods #
    # Container Methods
    def get_length(self):
        """Get the number of nodes in this container."""
        if self.is_empty:
            return 0
        else:
            length = 1
            node = self.first_node.next
            while node is not self.first_node:
                node = node.next
                length += 1
            return length

    def get_item(self, index):
        """Get a node based on its index from the start node."""
        node = self.first_node
        i = 0
        if index > 0:
            while i < index:
                node = node.next
                i += 1
        elif index < 0:
            index * -1
            while i < index:
                node = node.previous
                i += 1

        return node

    def append(self, data):
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.
        """
        if isinstance(data, LinkedNode):
            new_node = data
        else:
            new_node = LinkedNode(data)

        if self.first_node is None:
            self.first_node = new_node
        else:
            self.last_node.next = new_node
            self.first_node.previous = new_node

        return new_node

    def insert(self, data, index):
        """Add a new node and data at index within the nodes container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.
        """
        if isinstance(data, LinkedNode):
            new_node = data
        else:
            new_node = LinkedNode(data)

        if self.first_node is None:
            self.first_node = new_node
        else:
            point = self.get_item(index=index)
            new_node.next = point
            new_node.previous = point.previous
            new_node.previous.next = new_node
            point.previous = new_node

        return new_node

    def clear(self):
        """Clears this container by removing the first node."""
        self.first_node = None

    # Node Manipulation
    def move_node_start(self, node):
        """Move a node to the start of the container.

        Args:
            node: The node to move.
        """
        self.move_node_end(node)
        self.first_node = node

    def move_node_end(self, node):
        """Move a node to the end of container.

        Args:
            node: The node to move.
        """
        node.next.previous = node.previous
        node.previous.next = node.next
        node.next = self.first_node
        node.previous = self.last_node
        self.last_node.next = node
        self.first_node.previous = node

    def move_node(self, node, index):
        """Move a node to an index within the container.

        Args:
            node: The node to move.
            index: The place to move the node to.
        """
        node.next.previous = node.previous
        node.previous.next = node.next
        point = self.get_item(index=index)
        node.next = point
        node.previous = point.previous
        node.previous.next = node
        point.previous = node

    def shift_left(self, value=1):
        """Shift the start of nodes to the left by an amount.

        Args:
            value: The number of nodes to shift to the left.
        """
        if value == 1:
            self.first_node = self.first_node.next
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.next
                i += 1

    def shift_right(self, value=1):
        """Shift the start of nodes to the right by an amount.

        Args:
            value: The number of nodes to right to the left.
        """
        if value == 1:
            self.first_node = self.first_node.previous
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.previous
                i += 1
