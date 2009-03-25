#!/usr/bin/evn python

from voipy import base
from uri import Uri
import sip

# must have a generic class w/ support for arbitrary #'s of elements

# on first set to any of (method, uri, code, reason) switch class
class CmdLine(base.CmdLine):
    sep = ' '
    version = sip.SIPVERSION
    def __init__(self, buf=None, **kwargs):
        """CmdLine.__init__([buf], [method, [uri]], [code, [reason]])
        create a SIP message start line
        """
        super(CmdLine, self).__init__(buf, **kwargs)

    def parse(self, buf):
        try:
            p0,p1,p2 = buf.split(' ', 2)
            if p0.strip() == sip.SIPVERSION:
                self.code = p1
                self.reason = p2
                self.version = p0
            else:
                self.method = p0
                self.uri = p1
                self.version = p2
        except:
            raise

    def _loadargs(self, **kwargs):
        method = kwargs.get('method', None)
        uri = kwargs.get('uri', None)
        version = kwargs.get('version', sip.SIPVERSION)
        code = kwargs.get('code', None)
        reason = kwargs.get('reason', None)

        if (method or uri) and (code or reason):
            raise ValueError, "Cannot combine (method, uri) and (code, reason)"
        if method: self.method = method
        if uri: self.uri = uri
        if code: self.code = code
        if reason: self.reason = reason
        if version: self.version = version

    def isrequest(self):
        return isinstance(self, RequestLine)
    def isresponse(self):
        return not self.isrequest()

    def __setattr__(self, name, value):
        if name in ('method', 'uri'):
            self.__class__ = RequestLine().__class__
        elif name in ('code', 'reason'):
            self.__class__ = StatusLine().__class__
        if name == 'code' and type(name) == str:
            value = int(value)
        super(CmdLine, self).__setattr__(name, value)
    def pack(self):
        return self.version
    def __repr__(self):
        return self._repr(('version',))

class RequestLine(CmdLine):
    _uri = ''
    method = ''
    def _set_uri(self, uri):
        if not isinstance(uri, Uri):
            uri = Uri(uri)
        self._uri = uri
    uri = property(fget=lambda s: s._uri, fset=_set_uri, doc='Target URI')

    def pack(self):
        return self.sep.join([str(self.method),str(self.uri),str(self.version)])

    def __repr__(self):
        return super(RequestLine, self)._repr(('method', 'uri', 'version'))

class StatusLine(CmdLine):
    _code = ''
    reason = ''
    #more flexible to leave the int() up to the developer... 
    #def _set_code(self, code): self._code = int(code)
    #code = property(fget=lambda s:s._code, fset=_set_code, doc="Status Code")
    def pack(self):
       return self.sep.join([str(self.version),str(self.code),str(self.reason)])
    def __repr__(self):
        return super(StatusLine, self)._repr(('version', 'code', 'reason'))
