#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" directorytimeframeinterface.py
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
from abc import abstractmethod

# Third-Party Packages #

# Local Packages #
from ..timeseriesframe import TimeSeriesFrameInterface


# Definitions #
# Classes #
class DirectoryTimeFrameInterface(TimeSeriesFrameInterface):
    # Class Methods #
    @classmethod
    @abstractmethod
    def validate_path(cls, path):
        pass

    # Magic Methods
    # Construction/Destruction
    # def __init__(self, data=None, times=True, init=True):
    #     self.axis = 0
    #     self.sample_rate = 0
    #
    #     self.data = None
    #     self.times = None
    #
    #     if init:
    #         self.construct(data=data, times=times)

    # Instance Methods
    # Constructors/Destructors
    # def construct(self, data=None, times=None):
    #     if data is not None:
    #         self.data = data
    #
    #     if times is not None:
    #         self.times = times

    # Getters
    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    def get_item(self, item):
        pass

    @abstractmethod
    def get_time_axis(self):
        pass

    # Data
    @abstractmethod
    def get_range(self, start=None, stop=None, step=None):
        pass

    @abstractmethod
    def get_times(self, start=None, stop=None, step=None):
        pass  # return self.times[slice(start, stop, step)]

    # Find
    @abstractmethod
    def find_time_index(self, timestamp, aprox=False, tails=False):
        pass

    @abstractmethod
    def find_time_sample(self, timestamp, aprox=False, tails=False):
        pass

    # Shape
    @abstractmethod
    def validate_shape(self):
        pass

    @abstractmethod
    def change_size(self, shape=None, **kwargs):
        pass

    # Sample Rate
    @abstractmethod
    def validate_sample_rate(self):
        pass

    @abstractmethod
    def resample(self, sample_rate, **kwargs):
        pass

    # Continuous Data
    @abstractmethod
    def validate_continuous(self):
        pass

    @abstractmethod
    def make_continuous(self):
        pass
