
class RTPSocket():
    def write_audio(self, buf):
        hdr = self.default_hdr()

        hdr.sequence = self.next_sequence
        self.next_sequence += self.seq_incr

        hdr.body = buf
        self.send(str(hdr))

    def recv(self, pkt):
        hdr = pkt
        self.audio.write(hdr.buf)
