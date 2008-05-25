#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright  2008 Alberto Paro <alberto@ingparo.it>

"""
XML-RPC interface.
"""

import xmlrpclib
from datetime import datetime

def signature(*types):
    """
    Add a signature to a function or method.
    """

    def wrapper(func):
        """Save the signature."""
        func._signature = types
        return func

    return wrapper

