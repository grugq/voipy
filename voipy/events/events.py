#!/usr/bin/env python
# -*- coding: Latin-1 -*-
#
# Copyright 2006,2007 the grugq <grugq@hcunix.net>
#

import asyncore
import socket
import errno
import time


try:
    import pcap
    HAS_PCAP = True
except ImportError:
    # requires Dug Song's pypcap
    # http://code.google.com/p/pypcap/
    HAS_PCAP = False

class Handler(object):
    def __init__(self, channel=None):
        if channel:
            self.add_channel( channel )
    def add_channel(self, channel):
        channel.set_handler( self )

    def readable(self, channel): return True
    def writable(self, channel): return True

    def on_connect(self, channel): pass
    def on_accept(self, channel): pass
    def on_read(self, channel): pass
    def on_write(self, channel): pass
    def on_close(self, channel): pass
    def on_exception(self, channel): pass
    def on_process(self, channel): pass

class EventChannel(asyncore.dispatcher):
    def __init__(self, sock, handler):
        self.handler = handler
        asyncore.dispatcher.__init__(self, sock)
    def readable(self): return self.handler.readable(self)
    def writable(self): return self.handler.writable(self)
    def handle_connect(self): self.handler.on_connect(self)
    def handle_accept(self): self.handler.on_accept(self)
    def handle_read(self): self.handler.on_read(self)
    def handle_write(self): self.handler.on_write(self)
    def handle_close(self): self.handler.on_close(self)
    def handle_excpt(self): self.handler.on_exception(self)
    def handle_process(self): self.handler.on_process(self)

    def handle_error(self): raise

class UDPChannel(EventChannel):
    def __init__(self, handler=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        EventChannel.__init__(self, sock, handler)

    def sendto(self, data, tgt):
        try:
            result = self.socket.sendto(data, tgt)
            return result
        except socket.error, why:
            if why[0] == errno.EWOULDBLOCK:
                return 0
            else:
                raise
            return 0

    def recvfrom(self, buffer_size):
        try:
            data, addr = self.socket.recvfrom(buffer_size)
            if not data:
                # a closed connection is indicated by signaling
                # a read condition, and having recv() return 0.
                self.handle_close()
                return '', (None, None)
            else:
                return data, addr
        except socket.error, why:
            # winsock sometimes throws ENOTCONN
            if why[0] in (errno.ECONNRESET, errno.ENOTCONN, errno.ESHUTDOWN):
                self.handle_close()
                return '', (None, None)
            else:
                raise

    def safe_bind(self, addr, prange=100):
        host, port = addr

        for port in range(port+prange):
            try:
                self.bind((host, port))
            except:
                continue
            #except socket.error, why:
            #   if why[0] in(errno.EADDRINUSE,errno.EADDRNOTAVAIL,errno.EWOULDBLOCK):
            #       continue
            #   raise
        return host, port

class TCPChannel(EventChannel):
    def __init__(self, handler=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        EventChannel.__init__(self, sock, handler)
    def handle_connect(self):
        self.peeraddr = self.socket.getpeername()
        EventChannel.handle_connect(self)
    def recvfrom(self, buffer_size):
        buf = self.recv(buffer_size)
        return buf, self.peeraddr
    def sendto(self, buf, addr):
        return self.send(buf)

class SSLChannel(TCPChannel):
    def handle_connect(self):
        self.sslsock = socket.ssl( self.socket )
        EventChannel.__init__(self, sock, handler)
    def send(self, data):
        try:
            result = self.sslsock.write(data)
            return result
        except socket.error, why:
            if why[0] == EWOULDBLOCK:
                return 0
            else:
                raise
            return 0
    def recv(self, buffer_size):
        try:
            data = self.sslsock.read(buffer_size)
            if not data:
                self.handle_close()
                return ''
            return data
        # XXX could do something with finally ?
        except socket.error, why:
            # winsock sometimes throws ENOTCONN
            if why[0] in (errno.ECONNRESET, errno.ENOTCONN, errno.ESHUTDOWN):
                self.handle_close()
                return '', (None, None)
            else:
                raise

TLSChannel = SSLChannel

if HAS_PCAP:
    class PCAPChannel(EventChannel):
        def __init__(self, handle=None, name=None, filter=""):
            self.pcap_handle = pcap.pcap(name=name, immediate=True)
            self.pcap_handle.setnonblock()
            if filter:
                bpf = pcap.bpf(filter)
                self.pcap_handle.setfilter(bpf)
            fakesock = self.pcap_handle.fileno()
            EventChannel.__init__(self, fakesock, handle)

        def fileno(self):
            return self.pcap_handle.fileno()
        _fileno = property(fget=fileno, doc="file number")
        def writable(self): return False
        def readable(self): return True
        def handle_read(self):
            for tm,pkt in self.pcap_handle.readpkts():
                yield pkt

def Channel(proto, *args, **kwargs):
    if proto == 'udp':
        return UDPChannel(*args, **kwargs)
    elif proto == 'tcp':
        return TCPChannel(*args, **kwargs)
    elif proto in ('ssl', 'tls'):
        return SSLChannel(*args, **kwargs)
    elif proto == 'pcap' and HAS_PCAP:
        return PCAPChannel(*args, **kwargs)
    raise ValueError, 'Unknown channel protocol: %s' % proto

#############################################################################

class _sched(object):
    def __init__(self, func, delta):
        self.func = func
        self.delta = delta

class _scheduler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        # just so that we get scheduled. could also open a tmpfile...
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.time = time.time()
        self.scheduled = []
    def handle_connect(self):
        pass
    def handle_write(self):
        t = time.time()
        if long(t) == long(self.time):
            return
        diff = long(t) - long(self.time)

        for sched in self.scheduled:
            sched.delta -= diff
            if sched.delta <= 0:
                sched.func()
                self.scheduled.remove(sched)
    def schedule_func(self, func, delta):
        self.scheduled.append( _sched(func, delta) )

# XXX uncomment to enable scheduling (with 1 second precision, ouch!)
# _SCHEDULER = _scheduler()
def call_later(func, delta):
    _SCHEDULER.schedule_func( func, delta )

def run(timeout=0.5, count=None, map=None):
    # asyncore.loop(use_poll=True,**locals())
    asyncore.loop(timeout, use_poll=True, map=map, count=count)
