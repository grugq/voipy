#!/usr/bin/env python
# Author: the grugq <grugq@hcunix.net>
#

from voipy import base

# base class for all SIP objects
class SIPObject(base.VoIPyObject):
    def _loadargs(self, **kwargs):
        if kwargs and 'buffer' in kwargs:
            buffer = kwargs.get('buffer', None)
            if buffer:
                self.parse(buffer)
            del kwargs['buffer']

# constants go here:
VERSION="2.0"
SIPVERSION="SIP/2.0"
UDP="UDP"
TCP="TCP"

BRANCH_MAGIC="z9hG4bKac"
