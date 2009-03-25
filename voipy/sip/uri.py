#!/usr/bin/env python

import sip

# XXX dies horribly on NameAddrs... should warn?

def urisplit(uri):
    ''' -> (scheme, userpass, hostport, params, headers))
    scheme':' [userinfo '@'] hostport [';' uri-parameters] ['?' headers]
    '''
    def partition(S, sep):
        i = S.find(sep)
        if i > 0:
            return S[:i], sep, S[i+1:] # BUG, len(sep) > 1 ...
        return S, "", ""

    def splithostport(uri, start=0):
        for c in ';?':
            delim = uri.find(c)
            if delim >= 0:
                return uri[start:delim], uri[delim:]
        return uri, ""

    scheme,i,uri = partition(uri, ':')
    if not uri:
        uri = scheme
        scheme = 'sip'

    userpass,i,uri = partition(uri, '@')
    if not uri:
        uri = userpass
        userpass = ""

    hostport, uri = splithostport(uri)

    if len(uri):
        # if it is just headers
        if uri[0] == '?':
            params, headers = "", uri[1:]
        elif uri[0] == ';':
            if '?' in uri:
                params, headers = uri.split('?', 1)
            else:
                params, headers = uri, ""
    else:
        params, headers = "", ""

    return scheme,userpass,hostport,params,headers

class Uri(sip.SIPObject):
    scheme = 'sip'
    user = ''
    passwd = ''
    host = ''
    port = ''
    __slots__ = ('scheme','user','passwd','host','port','params','headers')

    #psep = ';'
    #hmark = '?'
    #hsep = ';'
    def __init__(self, buf=None, **kwargs):
        # TODO change the params from a dict() into a utils.SymbolicList()
        # TODO change the headers from a list() into a utils.SymbolicList()
        self.params = {} # lib.odict.odict()
        self.headers = {} # lib.odict.odict() ???
        super(Uri, self).__init__(buf, **kwargs)

    # is 'sip:6175550001' more legit than 'sip:127.0.0.1' ?
    def parse(self, buf):
        scheme,userpass,hostport,params,headers = urisplit(buf)

        self.scheme = scheme
        if ':' in userpass:
            self.user, self.passwd = urllib.splitpasswd(userpass)
        else:
            self.user, self.passwd = userpass, ''

        if ':' in hostport:
            self.host, self.port = urllib.splitport(hostport)
        else:
            self.host, self.port = hostport, 0

        if params:
            self.params.update([p.split('=', 1) for p in params.split(';')])
        if headers:
            self.headers.update([p.split('=', 1) for p in headers.split('&')])

    def pack(self):
        def pack_user():
            if self.user or self.passwd:
                s = self.user
                if self.passwd:
                    s += ':' + self.passwd
                return s + '@'
            return ''
        def pack_host():
            if self.port:
                return self.host + ':' + str(self.port)
            return self.host
        def _dump_dict(d, s):
            return s.join([ v and '%s=%s'%(k,v) or '%s='%(k,)
                    for k,v in d.iteritems()
                ])
        def pack_params():
            # FIXME use a user adjustable ';' -> self.psep ??
            if self.params:
                return ';' + _dump_dict(self.params, ';')
            return ''
        def pack_headers():
            if self.headers:
                return '?' + _dump_dict(self.headers, '&')
            return ''
        return '%s:%s%s%s%s'%(self.scheme, pack_user(), pack_host(),
                pack_params(), pack_headers())


if __name__ == "__main__":
    urilist = ['sip:bob@biloxi.com']

    u = Uri(urilist[0])

    print u.scheme, u.user, u.passwd, u.host, u.port, u.params, u.headers
    print '$', u, '$'
