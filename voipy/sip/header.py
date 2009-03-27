#!/usr/bin/env python

from voipy import utils
import values
import sip
from constants import headernames


class HeaderBase(sip.SIPObject):
    HCOLON = ":"
    sep = ","
    hname = ''
    _vclass = None

    name = property(fget=lambda s: headernames.normalize(s.hname))
    def __new__(cls, *args, **kwargs):
        obj = super(HeaderBase, cls).__new__(cls, *args, **kwargs)
        obj.values = []
        return obj

    def __init__(self, *args, **kwargs):
        if kwargs and 'hname' in kwargs:
            self.hname = kwargs['hname']
            del kwargs['hname']
        super(HeaderBase, self).__init__(*args, **kwargs)

        if not self.values:
            self.values.append( self._vclass(*args, **kwargs) )

    def _loadargs(self, *args, **kwargs):
        if kwargs and self.values:
            self.values[0].params.update(kwargs)

        #if args or kwargs:
            #    self.values.append( self._vclass(*args, **kwargs) )

    def parse(self, buf):
        for hv in utils.qsplit(buf, self.sep):
            self.values.append( self._vclass(hv) )

    def pack(self):
        return self.hname + self.HCOLON + ' ' + \
                self.sep.join([str(v) for v in self.values])

    def __getattr__(self, name):
        if hasattr(self, 'values'):
            if len(self.values) and hasattr(self.values[0], name):
                return getattr(self.values[0], name)
        raise AttributeError,name

    def __setattr__(self, name, value):
        if hasattr(self, 'values'):
            if len(self.values):
                return setattr(self.values[0], name, value)
        return super(HeaderBase, self).__setattr__(name, value)

    def __iter__(self):
        return iter(self.values)
    def __len__(self):
        return len(self.values)
    def __getitem__(self, index):
        return self.values[index]
    def __setitem__(self, index, value):
        if not issubtype(value, values.Value):
            value = self._vclass( value )
        self.values[index] = value

    #def __repr__(self):
        #return "%s<%s>" % (self.__class__.__name__, ', '.join([str(v)
            #for v in self.values]))

class Token(HeaderBase):
    """
    @value : An abitrary string value
    """
    _vclass = values.Token

class CallID(Token): pass
class String(Token): pass

class Expires(HeaderBase):
    """
    @value: A decimal value in seconds
    """
    _vclass = values.Expires

class Mime(HeaderBase):
    """
    @type: Major MIME type
    @sub_type: 'Minor MIME type
    """
    _vclass = values.Mime

class Int(HeaderBase):
    """
    @value: An integer value
    @comment: Optional comment
    """
    _vclass = values.Int

class GenericURI(HeaderBase):
    """
    @uri: Generic URI
    """
    _vclass = values.GenericURI

class NameAddr(HeaderBase):
    """
    display_name: Printable name
    uri: Generic URI
    """
    _vclass = values.NameAddr

class CSeq(HeaderBase):
    """
    sequence: Sequence number
    method: SIP METHOD
    """
    _vclass = values.CSeq

class Warning(HeaderBase):
    """
    code: Warning code
    hostname: Errant host system
    text: arbirary text tag
    """
    _vclass = values.Warning

class Via(HeaderBase):
    """
    protocol: default => 'SIP'
    version: default => '2.0'
    transport: default => 'UDP'
    host: default => 'localhost'
    port: default => None
    """
    _vclass = values.Via

class Auth(HeaderBase):
    """
    scheme:
    algorithm:
    cnonce:
    nonce:
    nc:
    opaque:
    qop:
    realm:
    response:
    stale:
    uri:
    username: 
    """
    _vclass = values.Auth
    def parse(self, buf):
        self.values.append( self._vclass(buf) )

# FIXME
class Date(HeaderBase):
    _vclass = values.Token
