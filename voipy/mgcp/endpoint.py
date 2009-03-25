#!/usr/bin/env python

import mgcp

class EndPoint(mgcp.MGCPObject):
    localname = '*'
    host = '*'
    port = None

    def parse(self, buf):
        # localname '@' host[:port]
         self.localname,self.host = buf.split('@',1)

         i = self.host.find(':')
         if i > 0:
             self.host = self.host[:i]
             self.port = self.port[i+1:]
    def _loadargs(self, **kwargs):
        for k in ('localname', 'host', 'port'):
            if k in kwargs:
                setattr(self, k, kwargs[k])
    def __repr__(self):
        return self._repr(('localname', 'host', 'port'))
    def pack(self):
        return '%s@%s%s' % (self.localname, self.host,
                                            self.port and ':'+self.port or '')

Any = EndPoint(localname='*', host='*')
