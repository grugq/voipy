#!/usr/bin/env python


from voipy import base
import constants
import endpoint

class CmdLine(base.CmdLine):
    # __members__ = ('verb', ... Use this sort of thing to make coding faster
    trans_id = 0
    def __init__(self, buf=None, **kwargs):
        '''__init__([buf], [verb, [version]], [trans_id], [code, reason]])

            @trans_id@ := transaction ID
        command keywords
            @verb@
            @version@ := default 'MGCP 1.0'
        response keywords
            @code@
            @reason@
        '''
        super(CmdLine, self).__init__(buf, **kwargs)
    def iscommand(self):
        return isinstance(self, CommandHeader)
    def parse(self, buf):
        try:
            verb = buf[:4]
            if verb.strip().isdigit(): # response code
                code,trans_id,buf = buf.split(None, 2) # code ' ' transid ' '[]
                self.code = code.strip()
                self.trans_id = trans_id.strip()
                if buf:
                    # 8xx response code includes '/'packageName
                    if self.code[0] == '8' and buf.lstrip()[0] == '/':
                        self.package,buf = buf.lstrip().split(None,1)
                    self.reason = buf
            else:
                verb,trans_id,endpoint,version=buf.split(None,3)
                self.verb = verb
                self.trans_id = trans_id
                self.endpoint = endpoint
                self.version = version
        except:
            raise

    def _loadargs(self, **kwargs):
        for k in ('verb', 'trans_id', 'endpoint', 'version', 'code',
                  'package', 'response'):
            if k in kwargs:
                setattr(self, k, kwargs[k])

    def __setattr__(self, name, value):
        if name in ('verb', 'endpoint', 'version'):
            self.__class__ = CommandHeader().__class__
        elif name in ('code', 'package', 'response'):
            self.__class__ = ResponseHeader().__class__
        super(CmdLine, self).__setattr__(name, value)
    def __repr__(self):
        return self._repr(('trans_id',))
    def pack(self):
        return self.trans_id

class CommandHeader(CmdLine):
    verb = ''
    trans_id = 0
    _endpoint = ''
    version = constants.MGCPVERSION

    def _set_endpoint(self, value):
        if not isinstance(value, endpoint.EndPoint):
            value = endpoint.EndPoint(value)
        self._endpoint = value
    endpoint=property(lambda s:s._endpoint, _set_endpoint,doc='EndPoint target')

    def __setattr__(self, name, value):
        super(CommandHeader, self).__setattr__(name, value)
    def pack(self):
        return ' '.join(['%s' % elem for elem in (self.verb, self.trans_id,
                                            self.endpoint, self.version)
                        if elem])
    def __repr__(self):
        return self._repr(('verb', 'trans_id', 'endpoint', 'version'))


class ResponseHeader(CmdLine):
    code = ''
    trans_id = ''
    package = None
    response = None

    def __setattr__(self, name, value):
        super(ResponseHeader, self).__setattr__(name, value)
    def pack(self):
        return ' '.join(['%s' % elem for elem in (self.code, self.trans_id,
                                            self.package, self.response)
                        if elem])
    def __repr__(self):
        return self._repr(('code', 'trans_id', 'package', 'response'))
