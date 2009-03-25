#!/usr/bin/env python

from voipy import base
from cStringIO import StringIO

import cmdline
import parameters
import headertable

class Message(base.Message):
    class Factory(base.Message.Factory):
        @staticmethod
        def cmdline(*args, **kwargs):
            return cmdline.CmdLine(*args, **kwargs)
        @staticmethod
        def header(*args, **kwargs):
            return parameters.Parameter(*args, **kwargs)
        @staticmethod
        def headertable(*args, **kwargs):
            return headertable.HeaderTable(*args, **kwargs)
        @staticmethod
        def body(*args, **kwargs):
            return str(*args)

    def __init__(self, buf=None, **kwargs):
        super(Message, self).__init__(buf, **kwargs)
        self.parameters = self.headers

    def parse(self, buf):
        str = StringIO(buf)

        def get_cmd_line():
            return str.readline().rstrip()
        def get_parameters():
            paramlist = []
            while True:
                l = str.readline()
                if not len(l.strip()):
                    break
                paramlist.append(l)
            return paramlist
        def get_body():
            return str.read()

        self.cmdline.parse( get_cmd_line() )
        self.headers += get_parameters()
        self.body += get_body()

    def _loadargs(self, **kwargs):
        for k in ('verb', 'trans_id', 'endpoint', 'version', 'code',
                  'package', 'response'):
            if k in kwargs:
                setattr(self.cmdline, k, kwargs[k])

    def pack(self):
        return '\n'.join(
            [str(self.cmdline)] +
            [str(hdr) for hdr in self.headers] +
            [''] +
            [str(self.body)])
