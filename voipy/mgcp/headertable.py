#!/usr/bin/env python

from voipy import base
import parameters

class HeaderTable(base.HeaderTable):
    def _get_key(self, key):
        if isinstance(key, parameters.Parameter):
            return key.name
        return key.upper() # no need to normalize, I guess.. 
    def _munge_value(self, value):
        if not isinstance(value, parameters.Parameter):
            value = parameters.Parameter(value)
        return value
