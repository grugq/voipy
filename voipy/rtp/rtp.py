#!/usr/bin/env python

import struct as _struct

_VERSION_MASK= 0xC000
_P_MASK     = 0x2000
_X_MASK     = 0x1000
_CC_MASK    = 0x0F00
_M_MASK     = 0x0080
_PT_MASK    = 0x007F
_VERSION_SHIFT=14
_P_SHIFT    = 13
_X_SHIFT    = 12
_CC_SHIFT   = 8
_M_SHIFT    = 7
_PT_SHIFT   = 0

VERSION = 2

class RTPHeader(object):
    _format = 'HHII'
    csrc = ''

    def _get_version(self): return (self._type&_VERSION_MASK)>>_VERSION_SHIFT
    def _set_version(self, ver):
        self._type = (ver << _VERSION_SHIFT) | (self._type & ~_VERSION_MASK)
    def _get_p(self): return (self._type & _P_MASK) >> _P_SHIFT
    def _set_p(self, p): self._type = (p << _P_SHIFT) | (self._type & ~_P_MASK)
    def _get_x(self): return (self._type & _X_MASK) >> _X_SHIFT
    def _set_x(self, x): self._type = (x << _X_SHIFT) | (self._type & ~_X_MASK)
    def _get_cc(self): return (self._type & _CC_MASK) >> _CC_SHIFT
    def _set_cc(self, cc): self._type = (cc<<_CC_SHIFT)|(self._type&~_CC_MASK)
    def _get_m(self): return (self._type & _M_MASK) >> _M_SHIFT
    def _set_m(self, m): self._type = (m << _M_SHIFT) | (self._type & ~_M_MASK)
    def _get_pt(self): return (self._type & _PT_MASK) >> _PT_SHIFT
    def _set_pt(self, m): self._type = (m << _PT_SHIFT)|(self._type&~_PT_MASK)

    version = property(_get_version, _set_version)
    p = property(_get_p, _set_p)
    x = property(_get_x, _set_x)
    cc = property(_get_cc, _set_cc)
    m = property(_get_m, _set_m)
    pt = property(_get_pt, _set_pt)

    def unpack(self, buf):
        self._type, self.seq, self.ts, self.ssrc = _struct.unpack('HHII', buf)
    def pack(self):
        return _struct.pack('HHII', self._type, self.seq, self.ts, self.ssrc)


class MediaStream():
    self.rtp_sock
    self.rtcp_sock

    self.cur_sequence
    self.session_id

    def recv_packet(self, pkt):
        if pkt.ssrc != self.session_id:
            return # ignore bad ssrc
        self.jitter_buf.append( pkt )
