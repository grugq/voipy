#!/usr/bin/env python
# @Author:      The Grugq (grugq@hcunix.net)

import sip
import uri

class Value(sip.SIPObject):
    sep=';'
    psep='='
    def __init__(self, *args, **kwargs):
        self.params = {}
        super(Value, self).__init__(*args, **kwargs)

    def _loadargs(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def parse(self, buf):
        elems = buf.split(self.sep, 1)
        if len(elems) > 0:
            self._do_value( elems[0].strip() )
        if len(elems) > 1 :
            self._do_params( elems[1] )
    def _do_value(self, value):
        pass
    def _do_params(self, params):
        # TODO change the self.params from a dict() into a utils.SymbolicList
        for param in params.split(self.sep):
            pn, pv = param.split(self.psep)

            self.params[pn] = pv
            # XXX note!! this clobbers
            #if self.params.has_key(pn):
                #self.params[pn].append(pv)
            #else:
                #self.params[pn] = [pv]
    def _pack_value(self):
        pass
    def _pack_params(self):
        if self.params:
            s = self.sep + self.sep.join(["%s%s%s"%(k,self.psep,v)
                for k,v in self.params.iteritems() ])
        else: s = ''
        return s
    def pack(self):
        return self._pack_value() + self._pack_params()

class Token(Value):
    value = ''
    def _do_value(self, value):
        self.value = value
    def _pack_value(self):
        return str(self.value)

class Expires(Token):
    def _loadargs(self, **kwargs):
        value = kwargs.get('value', None)
        if value:
            try:
                self.value = int(value)
            except:
                self.value = value
    def _do_value(self, value):
        try:
            self.value = int( value )
        except:
            self.value = value

class Mime(Value):
    type = ''
    sub_type = ''

    def _do_value(self, value):
        value = value.split('/', 1)
        self.type = value[0]
        if len(value) > 1:
            self.sub_type = value[1]
    def _pack_value(self):
        return self.type + (self.sub_type and '/%s' % self.sub_type)

class Int(Value):
    value = ''
    comment = ''

    def _loadargs(self, **kwargs):
        value = kwargs.get('value', None)
        if value is not None:
            try:
                self.value = int(value)
            except:
                self.value = value

    def _do_value(self, value):
        def get_int(buf):
            # FIXME this should be faster, and the checking is wrong
            # only the first character can be '-+'
            num = ""
            for c in buf.strip():
                if c not in '-+0123456789':
                    break
                num += c
            return long(num), buf[len(num):].strip()
        self.value, buf = get_int(value)

        if buf:
            # FIXME comment parsing is not very robust, e.g. '(xx) yy'
            self.comment = buf
            if self.comment[0] == '(':
                self.comment = buf[1:]
            else:
                self.comment = buf
            if self.comment[-1] == ')':
                self.comment = self.comment[:-1]

    def _pack_value(self):
        return str(self.value) + (self.comment and ' (%s)'%self.comment or '')

class GenericURI(Value):
    uri = ''
    def load(self, *args, **kwargs):
        if 'uri' not in kwargs:
            self.uri = uri.Uri()
        else:
            u = kwargs['uri']
            if isinstance(u, uri.Uri):
                self.uri = u
            else:
                try:
                    self.uri = uri.Uri(u)
                except:
                    pass
    def _do_value(self, value):
        buf = value.strip()

        laq = buf.find('<') + 1
        raq = buf.rfind('>')

        if raq == -1: raq = None

        self.uri = uri.Uri(buf[laq:raq])
    def _pack_value(self):
        # XXX should this be here, or in NameAddr() ??
        return str(self.uri)

class NameAddr(GenericURI):
    name = ''

    def _do_value(self, value):
        laq = value.find('<')
        raq = value.rfind('>')

        if laq != -1:
            self.name = value[:laq].strip()
        else:
            laq = None
        if raq == -1:
            raq = None
        super(NameAddr, self)._do_value(value[laq:raq])

    def _pack_value(self):
        return '%s <%s>' % (self.name, super(NameAddr, self)._pack_value())

class CSeq(Value):
    sequence = 0
    method = ''

    def _do_value(self, buf):
        l = buf.split(None, 1)
        try:
            seq = long(l[0])
        except:
            seq = l[0]
        self.sequence = seq
        if len(l) > 1:
            self.method = l[1]
    def _pack_value(self):
        # FIXME if not self.method, don't insert extra ' ' character
        return "%s %s" % (str(self.sequence), str(self.method))

class Warning(Value):
    code = ''
    hostname = ''
    text = ''
    def _do_value(self, buf):
        # XXX not robust XXX
        self.code, buf = buf.split(None, 1)
        self.hostname, buf = buf.split(None, 1)
        self.text = buf

    def _pack_value(self):
        return '%s %s "%s"' % (self.code, self.hostname, self.text)

class Via(Value):
    proto_sep = '/'
    protocol = 'SIP'
    version = sip.VERSION
    transport = sip.UDP
    host = ''
    port = 0

    def parse(self, buf):
        self._do_value(buf)

    def _do_value(self, buf):
        # FIXME not robust
        pvt, hp = buf.split()

        p, v, t = pvt.split(self.proto_sep)
        self.protocol = p
        self.version = v
        self.transport = t

        try:
            ndx = hp.rindex(':')
            host = hp[:ndx]
            port = long(hp[ndx+1:])
        except:
            host = hp
            port = 0

        self.host = host
        self.port = port

    def _pack_value(self):
        return '%s %s' % (
            self.proto_sep.join([self.protocol, self.version, self.transport]),
            (self.port and self.host + ':' + str(self.port) or self.host)
        )

class Auth(Value):
    scheme = ''
    algorithm = ''
    cnonce = ''
    nonce = ''
    nc = ''
    opaque = ''
    qop = ''
    realm = ''
    response = ''
    stale = ''
    uri = ''
    username = ''

    def parse(self, buf):
        self.scheme, buf = buf.split(None, 1)
        self.scheme.strip()
        for op in buf.split(','):
            name, value = op.split('=', 1)
            setattr(self, name.strip().strip('"'), value.strip().strip('"'))
    def _pack_value(self):
        return self.scheme + ' ' + ', '.join([('%s="%s"') % (k,v)
            for k,v in self.__dict__.iteritems()
            if not (callable(v) or k.startswith('_') or k in ('params', 'scheme'))])

class Date(Value):
    def _do_value(self, buf):
        pass
    def _pack_value(self):
        pass
