

class RegisterMessage(SCCPMessage):
    __hdr__ = (
        ('16s',   deviceName),
        ('I',   userid),
        ('I',   identifier),

