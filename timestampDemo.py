#!/usr/bin/env python3
# coding: utf-8
# File: timestampDemo.py
# Author: lxw
# Date: 4/20/17 6:14 PM


import time
import datetime

#strValue = datetime.datetime.now()
#d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")

d = datetime.datetime.now()
#d = d.isoformat(timespec='microseconds')
t = d.timetuple()
timeStamp = int(time.mktime(t)) * 1000
print(timeStamp)

#This one
timestamp = int(time.time() * 1000)