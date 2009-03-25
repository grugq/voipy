#!/usr/bin/env python

# list of keys for parsing order
# when building, include media_session_descriptor_blocks

class Message(sdp.SDP):
    sep = '\r\n'
    def __init__(self, *args, **kwargs):
        self.descriptors = []
        super(Message, self).__init__(*args, **kwargs)

        # self.current = global 
        # if descriptor.name == descriptors.Media:
        #   self.current = container.Container()
        #   self.containers.append( self.current )

    # actually, should a list of symbol tables too... for access
    # for each md in msg.media:
    #   for each attr in md[a]:
    #       do_something_attr()
    def parse(self, buf):
        pkt = utils.ParsingString(buf)

        for dline in pkt.readlines():
            self.descriptors.append( descriptor.Descriptor( dline ) )

    def pack(self):
        return self.sep.join([str(d) for d in self.descriptors])

    def __iter__(self): return iter(self.descriptors)
    def __len__(self): return len(self.descriptors)
