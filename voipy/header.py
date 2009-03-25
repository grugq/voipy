
class Header(object):
    def __init__(self): self.name = ''
    def __cmp__(self, other): return cmp(self.name, other.name)
    def __eq__(self, other): return self.name == other.name
    def __hash__(self): return hash(self.name)
