#!/usr/bin/env python

from voipy import sip
import events

# what happens when you call recvfrom() on a connected TCP socket?
#  it returns => (data, None)

# msgqueue needs to be more sophisticated, if a channel is connected, then store
# it the addr as the key for the msgqueue
# if the channel is not connected, use the channel as the key

# need much better channel management
#   sendmsg => lookup channel by addr, iff 'udp'
class UA(events.Handler):
    def open_channel(self, chantype='udp', connect_addr=None, bind_addr=None):
        chan = events.Channel(chantype, self)
        if bind_addr:
            chan.bind(bind_addr)
        if connect_addr:
            chan.connect(connect_addr)
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

class UAC(UA): pass
class UAS(UA): pass
