#! /usr/bin/env python

from collections import namedtuple as _namedtuple

ProcStatus = _namedtuple('ProcStatus', 'stdout stderr returncode')
