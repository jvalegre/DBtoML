#!/usr/bin/env python

"""
##################################################
#          __main__ file for the code            #
##################################################
"""

from __future__ import absolute_import

import os
import sys

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl

if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from pyconfort import pyconfort

if __name__ == '__main__':
    sys.exit(pyconfort.main())
