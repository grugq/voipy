#!/usr/bin/env python
# @author: the grugq <grugq@hcunix.net>
# copyright 2006, 2007 the grugq <grugq@hcunix.net>

class Descriptor(sdp.SDP):
    dname = ''
    dsep = '='
    def __init__(self, *args, **kwargs):
        pass

    def parse(self, buf):


class Version(Descriptor):
    dname = 'v'
    version = sdp.VERSION
