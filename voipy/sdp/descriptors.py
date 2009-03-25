#!/usr/bin/env python

class _MetaDescriptor(type):
    def __new__(clsobj, clsname, clsbases, clsdict):
        obj = super(_MetaDescriptor, clsobj).__new__(clsobj,clsname,clsbases,clsdict)

        if hasattr(obj, '__content__ '):
            obj.__content_order__ = [x[0] for x in obj.__content__]
            obj.__dict__.update(dict(obj.__content__))
        return obj

class Descriptor(sdp.SDP):
    __metaclass__ = _MetaDescriptor
    dname = ''
    dsep = '='

    _sep = None

    def parse(self, buf):
        l = buf.split(self._sep)
        n = [x[0] for x in self.__content__]
        for k,v in itertools.izip(n, l):
            setattr(self, k, v)

    def pack(self):
        content = ''
        if '__content_order__' in self.__dict__:
            n = [x[0] for x in self.__content_order__]
            content =  ' '.join([str(getattr(self, s)) for s in n])
        return '%s%s%s' % (self.dname, self.dsep, content)


class Version(DescriptorBase): # 'v'
    dname = 'v'
    __content__ = (
        ('version', sdp.VERSION),
    )

class Origin(DescriptorBase): # 'o'
    dname = 'o'
    __content__ = (
        ('username', ''),
        ('sessid', ''),
        ('version', ''),
        ('nettype', 'IN'),
        ('addrfamily', 'IP4'),
        ('ipaddr', ''),
    )

class SessionName(DescriptorBase): # 's'
    dname = 's'
    __content__ = (
        ('sessname', ''),
    )

class Information(DescriptorBase): # 'i'
    dname = 'i'
    __content__ = (
        ('info', ''),
    )

class Uri(DescriptorBase): # 'u'
    # TODO expand to provide full host, port, username, passwd
    dname = 'u'
    __content__ = (
        ('uri', ''),
    )

# Email + Phone support a "comment" after the content...
class Email(DescriptorBase): # 'e'
    dname = 'e'
    # TODO expand to provide full email addr support, name, username, host, 
    __content__ = (
        ('email', ''),
    )

class Phone(DescriptorBase): # 'p'
    dname = 'p'
    # TODO full international style support, country code, elems, etc? '+', '-'
    __content__ = (
        ('number', ''),
    )


class Connection(DescriptorBase): # 'c'
    dname = 'c'
    # TODO create a proper address class with 'ip', 'ttl', 'num addrs' sep='/'
    __content__ = (
        ('nettype', 'IN'),
        ('addrtype', 'IP4'),
        ('ipaddr', ''),
    )

class Bandwidth(DescriptorBase): # 'b'
    dname = 'b'
    _lookup = {
            'CT' : 'Conference Total'
            'AP' : 'Application Specific'
    }
    __content__ = (
        ('modifier', 'AP'),
        ('value', '')
    )
    _sep = ':'
    def pack(self):
        s = super(Bandwidth, self).pack()
        return s + '%s:%s' % (self.modifier, self.value)

class Time(DescriptorBase): # 't'
    dname = 't'
    __content__ = (
        ('start', 0),
        ('stop', 0)
    )
    # NTP time, convert to unix time by +/- 2208988800

class Repeat(DescriptorBase): # 'r'
    dname = 'r'
    # TODO a repeat value parser, (d), (h), (m), (s)
    __content__ = (
        ('iterval', 0),
        ('duration', 0),
        ('offsets', []),
    )
    def parse(self, buf):
        l = buf.split()
        try:
            self.iterval = l.pop(0)
            self.duration = l.pop(0)
            self.offsets = l
        except:
            return
    def pack(self):
        return self.dname + self.dsep + '%s %s %s' % (self.iterval,
                self.duration, ' '.join([str(s) for s in self.offsets]))

class Zone(DescriptorBase):
    # TODO timezone parser, list of zone objects 'adjustment' + 'offset'
    dname = 'z'
    __content__ = (
        ('adjustment', 0),
        ('offset', 0),
    )
    # break into list of lists? or list of objects?

class Key(DescriptorBase):
    dname = 'k'
    # TODO support for base64, uri, prompt Key types
    __content__ = (
        ('method', 'clear'),
        ('key', ''),
    )
    _sep = ':'
    def pack(self):
        k = ''
        if self.key:
            k = ':' + str(self.key)
        return self.dname + self.dsep + self.method + k

class Attribute(DescriptorBase):
    dname = 'a'
    __content__ = (
        ('attribute', ''),
        ('value', ''),
    )
    _sep = ':'
    def pack(self):
        v = ''
        if self.value:
            v = self._sep + str(self.value)
        return self.dname + self.dsep + self.attribute + v

# XXX
# a=<type>/<subtype> # MIME

# a=recvonly
# a=sendrecv
# a=sendonly

# a=rtpmap:<payload type> <encoding name>/<clock rate>[/<encoding params>]
# a=cat:<category>
# a=keywds:<keywords> # ' ' seperated list
# a=tool:<name and version of tool>
# a=ptime:<packet time> # time in milliseconds
# a=orient:<whiteboard orientation>
# a=type:<conference type> # `broadcast', `meeting', `moderated', `test', `H332'
# a=charset:<character set>
# a=sdplang:<language tag>
# a=lang:<language tag>
# a=framerate:<frame rate>
# a=quality:<quality> # 0 -> 10 (0 worst, 10 best)
# a=fmtp:<format> <format specific parameters>

class Media(DescriptorBase):
    dname = 'm'
    # TODO fix this!#
    # mediatypes = 'audio', 'video', 'application', 'data', 'control'
    # transport = 'RTP/AVP', 'udp'
    __content__ = (
        ('media', 'audio'),
        ('port', ''),
        ('transport', 'RTP/AVP'),
        ('fmt', []),
    )
    # num_ports == optional, 'port/num'
    def parse(self, buf):
        pass
    def pack(self):
        pass
