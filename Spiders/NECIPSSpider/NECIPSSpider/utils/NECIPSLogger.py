#!/usr/bin/env python3
# coding: utf-8
# File: NECIPSLogger.py
# Author: lxw
# Date: 5/10/17 10:25 AM

import logging
import os

logging.basicConfig(level=logging.DEBUG, filemode="w")


# class NECIPSLogger(logging.Logger):   # No need
# TODO: singleton
class NECIPSLogger():
    def __init__(self, logger_name):
        self.logger_name = logger_name

    def generate(self):
        my_logger = logging.getLogger(self.logger_name)
        file_name = os.path.join(os.getcwd(), self.logger_name+".log")
        """
        if os.path.isfile(file_name):
            with open(file_name, "w"):
                pass
        """
        fh = logging.FileHandler(file_name)
        formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
        fh.setFormatter(formatter)
        my_logger.addHandler(fh)
        return my_logger