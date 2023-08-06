#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" versiontype.py
A dataclass like object that contains a str name and associated class for a version. See versions for examples of
implementation.
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

# Third-Party Packages #
from baseobjects import BaseObject

# Local Packages #


# Definitions #
# Classes #
class VersionType(BaseObject):
    """A dataclass like object that contains a str name and associated class for a version.

    Attributes:
        name (str, optional): The string name of this object.
        class_ (:class:, optional): The class of the version.

    Args:
        name (str): The string name of this object.
        class_ (:class:): The class of the version.
    """
    __slots__ = ["name", "class_"]

    # Construction/Destruction
    def __init__(self, name=None, class_=None, init=True):
        self.name = None
        self.class_ = None

        if init:
            self.construct(name=name, class_=class_)

    # Representation
    def __hash__(self):
        """Overrides hash to make the object hashable.

        Returns:
            The system ID of the object.
        """
        return id(self)

    # Type Conversion
    def __str__(self):
        """Returns the str representation of the version.

        Returns:
            str: A str with the version numbers in order.
        """
        return self.name

    # Comparison
    def __eq__(self, other):
        """Expands on equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is equivalent.
        """
        if isinstance(other, type(self)):
            return other.name == self.name
        if isinstance(other, str):
            return other == self.name
        else:
            return super().__eq__(other)

    def __ne__(self, other):
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is not equivalent.
        """
        if isinstance(other, type(self)):
            return other.name != self.name
        if isinstance(other, str):
            return other != self.name
        else:
            return super().__ne__(other)

    # Methods
    def construct(self, name=None, class_=None):
        """Constructs the version type object based on inputs.

        Args:
            name (str, optional): The string name of this object.
            class_ (:class:, optional): The class of the version.
        """
        self.name = name
        self.class_ = class_
