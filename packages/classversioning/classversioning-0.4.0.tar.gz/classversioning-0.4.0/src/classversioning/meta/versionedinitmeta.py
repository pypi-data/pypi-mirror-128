#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" versionedinitmeta.py
Description:
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
from baseobjects import InitMeta

# Local Packages #
from .versionedmeta import VersionedMeta


# Definitions #
# Meta Classes #
class VersionedInitMeta(InitMeta, VersionedMeta):
    """A mixed class of the InitMeta and VersionMeta."""
    ...
