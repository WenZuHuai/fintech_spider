#!/usr/bin/env python3
# coding: utf-8
# File: error.py
# Author: lxw
# Date: 4/27/17 1:41 PM


class ResourceDepletionError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy source is exhausted.')


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr("The proxy pool is empty.")
