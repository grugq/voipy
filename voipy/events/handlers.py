#!/usr/bin/env python
#
# (c) Copyright 2006, 2007 the grugq <grugq@hcunix.net>
#

from voipy import sip
import events


class SipHandler(events.Handler):
    def __init__(self, channel=None):
        super(SipHandler, self).__init__(channel)
        self.channels = []
        if channel:
            self.channels.append(channel)
    def open_channel(self, chantype='udp', connect_addr=None, bind_addr=None):
        chan = events.Channel(chantype, self)
        if bind_addr:
            chan.bind(bind_addr)
        if connect_addr:
            chan.connect(connect_addr)
        self.channels.append(chan)
        return chan

    def on_read(self, channel):
        data, addr = channel.recvfrom(653556)
        addr = addr or channel.addr
        msg = sip.message.Message( buffer=data )
        self.recvmsg(msg, addr)

    def sendmsg(self, msg, addr):
        pass
    def recvmsg(self, msg, addr):
        pass

# msgqueue needs to be more sophisticated, if a channel is connected,then store
# it the addr as the key for the msgqueue
# if the channel is not connected, use the channel as the key

# need much better channel management
#   sendmsg => lookup channel by addr, iff 'udp'

class UA(SipHandler): pass
class UAC(UA): pass
class UAS(UA): pass

#############################################################################

class Monitor(events.Handler):
    pass
