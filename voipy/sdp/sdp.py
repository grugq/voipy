#!/usr/bin/env python

from voipy import voipacket

class SDP(voipacket.VoIPy):
    pass

VERSION   ="1.0"
ORIGIN    =  "o"
SESSION   =  "s"
INFORMATION= "i"   # optional
URI       =  "u"   # optional
EMAIL     =  "e"   # optional
PHONE     =  "p"   # optional
CONNECTION=  "c"   # optional if provided in media descriptions
BANDWIDTH =  "b"   # optional
TIMEZONE  =  "z"   # optional
KEY       =  "k"   # optional
ATTRIBUTE =  "a"   # optional
