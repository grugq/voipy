#!/usr/bin/env python

from voipy import base

import cmdline
import header as headerbases
import headers
from constants import headernames
from cStringIO import StringIO

class HeaderTable(base.HeaderTable):
    def _get_key(self, key):
        if not isinstance(key, headerbases.HeaderBase):
            key = headernames.normalise(key)
        else:
            key = key.name
        return key
    def _munge_value(self, value):
        if not isinstance(value, headerbases.HeaderBase):
            try:
                value = headers.Header(value)
            except:
                raise KeyError, "Could not convert '%r' to Header object"\
                        % value
        return value

class Message(base.Message):
    class Factory(base.Message.Factory):
        @staticmethod
        def cmdline(*args, **kwargs): return cmdline.CmdLine(*args, **kwargs)
        @staticmethod
        def headertable(*args, **kwargs): return HeaderTable(*args, **kwargs)
        @staticmethod
        def header(*args, **kwargs): return headers.Header(*args, **kwargs)
        @staticmethod
        def body(buf=''): return buf # should be a MIME message

    sep = '\r\n'
    start = property(lambda s: s.cmdline, lambda s,v: s.cmdline.parse(v),
                                                        'Request/Status Line')
    startline=start
    def __init__(self, buf=None, *args, **kwargs):
        """__init__([buf], [method, [uri], [code, [reason]]) => SIPMessage
        Create a new SIP message object
        Optionally, pass in one of the following args

        positional
            @buf@ := buffer containing a packed SIP message
        keyword
            @method@ := string to set as SIP message method
            @uri@ := target URI for message
            @code@ := status code
            @reason@ := reason string
        """
        super(Message, self).__init__(buf, *args, **kwargs)
        self.__initialized = True


    def _loadargs(self, **kwargs):
        method = kwargs.get('method', None)
        uri = kwargs.get('uri', None)
        version = kwargs.get('version', None)
        code = kwargs.get('code', None)
        reason = kwargs.get('reason', None)
        buffer = kwargs.get('buffer', None)

        if method: self.start.method = method
        if uri: self.start.uri = uri
        if version: self.start.version = version
        if code: self.start.code = code
        if reason: self.start.reason = reason
        if buffer:
            self.parse(buffer)


    def parse(self, buf):
        str = StringIO(buf)

        def get_start_line():
            return str.readline().rstrip()
        def get_headers():
            import headers
            curr = ''
            hl = []

            while True:
                line = str.readline().strip()
                if not len(line): break

                if curr:
                    curr += ' '
                curr += line

                pos = str.tell()
                if pos == len(buf):
                    hl.append( curr )
                    break

                if str.read(1) in ' \t':
                    str.seek(pos)
                    continue
                str.seek(pos)
                hl.append( curr )
                curr = ''
            return [headers.Header(h) for h in hl]

        def get_body():
            return str.read()

        self.cmdline.parse( get_start_line() )
        self.headers += get_headers()
        self.body = self.Factory.body( get_body() )

        if self.cmdline.isresponse():
            self.response = self.cmdline
        else:
            self.request = self.cmdline

    def __iadd__(self, hdr):
        if isinstance(hdr, cmdline.CmdLine):
            self.start = hdr
        else:
            self.headers += hdr
        return self
    def __getitem__(self, name):
        return self.headers[name]
    def __setitem__(self, name, other):
        self.headers[name] = other

# For some reason, self.__dict__ only has '_Message__initialized' = True
# My current feeling is that this functionality is non-critical,
# and can be left out until later
#
# __iadd__() calls __setattr__() after it finishs computing
# this means msg.headers = headers ... can't think of how to handle this
# elegantly
    #def __setattr__(self, key, value):
        #if not self.__dict__.has_key('_Message__initialized') or \
        #        self.__dict__.has_key(key):
    #        return super(Message, self).__setattr__(key, value)
        #hdr = headers.Header(hname=key, value=value)
        #self.headers += headers.Header(hname=key, value=value)
        #setattr(self.headers, key, value)
    def __getattr__(self, name):
        if name in self.__dict__:
            return super(Message, self).__getattr__(name)
        elif hasattr(self, 'headers'):
            try:
                value = self.headers[name]
                if len(value) == 1:
                    value = value[0]
                return value
            except KeyError:
                pass
        raise AttributeError('No such header: %s' % name)

    def pack(self):
        if self.start:
            s = str(self.start) + self.sep
        if self.headers:
            s += self.sep.join([str(hdr) for hdr in self.headers])
        s += self.sep
        if self.body:
            s += str(self.body) + self.sep
        return s
