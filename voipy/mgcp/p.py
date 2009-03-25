from pyparsing import *

tp="L/dh(f(m=1000,h(900)),b(ss/t(sendrecv)))"

eventId = Word(alphanums + '-')
eventRange = '[' + (Word(alphanums) ^ \
                    (Word(alphanums) + '-' + Word(alphanums))) + ']'
eventName = Optional( (Word(alphanums) ^ '*') + '/') + \
        (eventId ^ CaselessKeyword('all') ^ eventRange ^ '*' ^ '#') + \
        Optional("@" + (Word(alphanums) ^ '*' ^'$'))

requestedActions = delimitedList(requestedAction)

print eventName.parseString(tp)
