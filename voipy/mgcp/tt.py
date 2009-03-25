tp="L/dh([555555-99999], f(7777, g(hh(8989),ii(echo))), y=9000)"

class Event(object):
    def __init__(self, name):
        self.name = name
        self.params = []
    def __str__(self):
        return "event('%s', %r)" % (self.name, self.params)
    __repr__ = __str__

def breakup(instr):
    stack = []
    cur = ''
    event = None

    stack.append(event)
    for c in instr:
        if c == '(':
            # new parameter
            print "#event#", cur
            e = Event(cur)
            stack.append(e)
            event.params.append(e)
            cur = ''
        elif c == ')':
            # end of parameter
            e.params.append(cur)
            cur = ''
            e = stack.pop()
        elif c == ',':
            if cur:
                e.params.append(cur)
                cur = ''
        else:
            cur += c
    return event


def parseuntil(instr, starttok=')', endtok=')'):
    stack = []
    cur = ''
    for ndx in range(len(instr)):
        c = instr[ndx]
        if c == '(':
            stack.append( parseuntil(instr[ndx+1:]) )
        elif c == ',':
            stack.append(cur)
            cur = ''
        elif c == ')':
            stack.append(cur)
            return stack
        else:
            cur += c
    stack.append(cur)
    return stack

def main():
    #print parseuntil(tp)
    print breakup(tp)

main()
