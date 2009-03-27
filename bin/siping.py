#!/usr/bin/env python

import urllib
from voipy.events import useragent, events
from voipy import sip
from optparse import OptionParser

# METHOD
# -m{} --method {}
def method_options(parser):
    def method_callback(option, opt_str, value, parser):
        quick_methods = { 'A' : 'ACK', 'B' : 'BYE', 'C' : 'CANCEL',
            'O' : 'OPTIONS', 'I' : 'INVITE', 'R' : 'REGISTER', }
        if len(parser.rargs) and parser.rargs[0][0] != '-': # Buggy for last option?
            parser.values.target_uri = parser.rargs.pop(0)
        parser.values.method = quick_methods.get(value.upper(), value)
 
    parser.add_option('-m', '--method', action="callback", callback=method_callback,
            type="string", dest="method", default="OPTIONS",
            help="Method for SIP utils message") 
    return parser

# Headers
# -C --contact uri
# -F --from uri
# -T --to uri
def core_header_options(parser):
    parser.add_option('-C', '--contact', action="append", dest="contacts_uri",
            default=[], help="Contacts URI")
    # TODO change from 'store' => 'append', allowing multiple To/From fields
    parser.add_option('-F', '--from', action="store", dest="from_uri",
            default='"siping" <sip:siping@localhost>', help="From URI")
    parser.add_option('-T', '--to', action="store", dest="to_uri",
            #default="'siping' <sip:siping@localhost>",
            help="To URI")
    return parser

# --via host:port
# --expires seconds
# --max-forwards count
# --cseq count[:method]
# --content-length count
# --callid string
def opt_header_options(parser):
    def cseq_callback(option, opt_str, value, parser):
        if len(value.split(None, 1)) == 2:
            setattr(parser.values, 'cseq_seq', value.split()[0])
            setattr(parser.values, 'cseq_method', value.split(None,1)[1])
        elif value.isdigit():
            setattr(parser.values, 'cseq_seq', int(value))
        else:
            setattr(parser.values, 'cseq_method', value)
    parser.add_option('--cseq', action="callback", callback=cseq_callback, 
            type="string", help="CSeq: count [method]")
    parser.add_option('--cseq-sequence', dest="cseq_seq", type="int",
            help="CSeq: seq_cnt", default=1)
    parser.add_option('--cseq-method', dest="cseq_method", 
            help="CSeq: METHOD")

    parser.add_option('--via', action="store", dest="via", 
            help="Via: host[:port]")
    # other via stuff? probably best to have a via section => v2

    parser.add_option('--expires', type="int", dest="expires", default=None,
            help="Expires: num_seconds")
    parser.add_option('--content-length', dest="content_length", type="int",
            default=0, help="Content-Length: count")
    parser.add_option('--callid', dest='callid', help='CallID: id_string')
    parser.add_option('--max-forwards', dest="max_forwards", type="int", 
            default=70, help="Max-Forwards: count")

    return parser

# -t target_host:port
# -u --user username
# -p --passwd password
# -w --wait count
# -c --count number_msgs
# --body ['-'|fp|str]
def application_options(parser):
    def addr_callback(option, opt_str, value, parser):
        host, port = urllib.splitnport(value, 5060)
        setattr(parser.values, option.dest, (host,port))
    def body_callback(option, opt_str, value, parser):
        if len(value) == 1 and value == '-':
            value = sys.stdin
        else:
            value = open(value, 'r')
        parser.values.body = value # XXX should be an async file IO object

    def proto_callback(option, opt_str, value, parser):
        if opt_str == '--udp':
            parser.values.proto = 'udp'
        elif opt_str == '--tcp':
            parser.values.proto = 'tcp'
        elif opt_str in ('--ssl', '--tls'):
            parser.values.proto = 'ssl'

    parser.add_option('--uri', dest="target_uri", help="Target URI")

    # possibly do: siping <args> [user:password@]target_host[:port]
    parser.add_option('-t', '--target', action="callback", callback=addr_callback,
            help="host[:port]", dest="target")
    parser.add_option('--bind', action="callback", callback=addr_callback,
            dest="bind_addr", help="bind_host[:port]")
    parser.add_option('--udp', '--tcp', '--ssl', '--tls', action="callback",
            callback=proto_callback, dest="proto", default="udp",
            help="select transport protocol")
    parser.add_option('-u', '--user', dest="username", help="username")
    parser.add_option('-p', '--passwd', dest="passwd", help="password")
    parser.add_option('-w', '--wait', type="int", dest="wait", default=1,
            help="seconds to await response")
    parser.add_option('-c', '--count', type="int", dest="count", default=1,
            help="number of messages to send, negative == non-stop")
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose",
            default=False, help="Verbosity toggle")
    parser.add_option('--body', action="callback", callback=body_callback,
            help="body of the message: filename, or -")
    parser.add_option('--trace', action="store_true", dest="traceroute",
            default=False, help="Perform a SIP traceroute")
    parser.add_option('--register', action="store_true", dest="register",
            default=False, help="Authenticate with a Registrar")
    return parser

def build_parser():
    parser = OptionParser()
    method_options(parser)
    core_header_options(parser)
    opt_header_options(parser)
    application_options(parser)
    return parser

class Siping(useragent.UAC):
    def __init__(self, config):
        super(Siping, self).__init__()

        self.config = config
        self.channel = self.open_channel(config.proto, config.target_addr)

    def close(self):
        self.channel.close()

    def sendmsg(self, msg, addr=None):
        print '>' * 30, 'localhost:', '>' * 30
        print msg
        print '>' * 75
        if addr:
            return self.channel.sendto(str(msg), addr)
        return self.channel.send(str(msg))

    def recvmsg(self, msg, addr):
        print '<' * 30, '%s:%s' % addr, '<' * 30
        print msg
        print '<' * 75

    def build_msg(self):
        from voipy.sip import utils
        def base_message():
            method = self.config.method
            turi = self.config.target_uri
            msg=sip.message.Message(method=method,uri=sip.values.NameAddr(turi).uri)
            return msg
        def core_headers(msg):
            msg += sip.headers.To( self.config.to_uri )
            msg += sip.headers.From( self.config.from_uri, tag=utils.compute_tag() )
            for contact_uri in self.config.contacts_uri:
                msg += sip.headers.Contact( contact_uri ) # XXX do 1 header
        def via_headers(msg):
            msg += sip.utils.make_via()
            if self.config.via:
                msg.via.host, msg.via.port = urllib.splitnport(self.config.via, 5060)
        def add_headers(msg):
            msg += sip.headers.MaxForwards(value=self.config.max_forwards)
            if self.config.expires != None:
                msg += sip.headers.Expires(value=self.config.expires)
            msg += sip.headers.CSeq(sequence=self.config.cseq_seq,
                    method=self.config.cseq_method)
            msg += sip.headers.ContentLength( value=self.config.content_length )

            callid = self.config.callid or sip.utils.compute_call_id()
            msg += sip.headers.CallId( value=callid )

        msg = base_message()
        core_headers( msg )
        via_headers( msg )
        add_headers( msg )
        return msg

# Send 1..n packets to a target server
class OptionsPing(Siping):
    def __init__(self, *args, **kwargs):
        super(OptionsPing, self).__init__(*args, **kwargs)
        self.waitcnt = 1

    def writable(self, channel):
        return self.config.count != 0

    def recvmsg(self, msg, addr):
        super(OptionsPing, self).recvmsg(msg, addr)

        if msg.response.code in (401,403,404,407):
            if 'www-authenticate' in msg.headers:
                amsg = self.build_msg()
                amsg.headers['call-id'].value = msg.headers['call-id'].value
                amsg += sip.utils.make_authorisation(
                        msg.headers['www-authenticate'], amsg.request.method,
                        str(amsg.request.uri),
                        self.config.username, self.config.passwd
                        )
                self.sendmsg(amsg)
                self.waitcnt += 1

    def on_write(self, channel):
        if self.config.count != 0:
            msg = self.build_msg()
            self.sendmsg(msg)
            self.config.count -= 1

    def on_process(self, channel):
        if self.config.count == 0:
            if not self.waitcnt:
                self.close()
            else:
                self.waitcnt -= 1

class TracerPing(Siping):
    def __init__(self, *args, **kwargs):
        self.curr_maxfwds = 1
        self.max_maxfwds = 70
        self.waitcnt = 1
        super(TracerPing, self).__init__(*args, **kwargs)

    def writable(self, channel):
        return self.curr_maxfwds < self.max_maxfwds

    def on_process(self, channel):
        if self.max_maxfwds == self.curr_maxfwds:
            if not self.waitcnt:
                self.close()
            else:
                self.waitcnt -= 1

    def on_write(self, channel):
        msg = self.build_msg()
        msg.headers['max-forwards'].value = self.curr_maxfwds
        self.sendmsg(msg)
        self.curr_maxfwds += 1

class RegisterPing(Siping):
    def __init__(self, *args, **kwargs):
        super(RegisterPing, self).__init__(*args, **kwargs)

    def on_connect(self, channel):
        self.state = 'unauth'

    def writable(self, channel):
        return self.state in ('unauth', 'auth')

    def on_write(self, channel):
        if self.state == 'unauth':
            msg = self.build_msg()
            self.sendmsg(msg)

    def recvmsg(self, msg, addr):
        super(RegisterPing, self).recvmsg(msg, addr)
        if msg.response.code in (401,404,407) and \
                'www-authenticate' in msg.headers:
            authmsg = sip.request.RegisterAuthorisation( msg, self.config.username,
                    self.config.passwd)
            self.state = 'waiting'
            self.sendmsg(authmsg)
        else:
            self.close()

def sane_config(options):
    if not options.target_uri and not options.to_uri:
        options.target_uri = options.to_uri = '"siping" <sip:siping@localhost>'
    elif options.target_uri and not options.to_uri:
        options.to_uri = options.target_uri
    elif options.to_uri and not options.target_uri:
        options.target_uri = options.to_uri

    #if not options.target_uri: options.target_uri = options.to_uri
    if not options.from_uri: options.from_uri = options.to_uri
    if not options.contacts_uri: options.contacts_uri.append( options.from_uri )

    if not options.cseq_method:
        options.cseq_method = options.method

    if not hasattr(options, 'target_addr'):
        hp = options.to_uri.find('sip:')
        hp = options.to_uri[hp+4:]
        if '@' in hp:
            up, hp = urllib.splituser(hp)

        if hp[-1] == '>': hp = hp[:-1]

        h, p = urllib.splitnport(hp, 5060)

        if type(p) != int: p = int(p)

        setattr(options, 'target_addr', (h, p))

        if up:
            u, p = urllib.splitpasswd(up)
            setattr(options, 'username', u)
            setattr(options, 'password', p)

    if not options.target_addr[1]: # no port
        options.target_addr = (options.target_addr[0], 5060)

def check_args(options, args):
    if not args:
        return
    # someway to test if it is a SIP URI
    if 'sip:' in args[0]:
        setattr(options, 'target_uri', args[0])

    userpass, hostport = urllib.splituser(args[0])

    if hostport[:4] == 'sip:': hostport = hostport[4:]
    host, port = urllib.splitnport(hostport, 5060)
    # XXX Overwrites!
    setattr(options, 'target_addr', (host, port))

    if userpass:
        user, passwd = urllib.splitpasswd(userpass)
        user and setattr(options, 'user', user)
        passwd and setattr(options, 'passwd', passwd)

def parse_config():
    parser = build_parser()
    options, args = parser.parse_args()
    check_args( options, args )
    sane_config( options )

    return options

def main():
    config = parse_config()

    if not config.proto:
        config.proto = 'udp'
    #config.register = False

    if config.traceroute:
        pinger = TracerPing(config)
    elif config.register:
        pinger = RegisterPing(config)
    else:
        pinger = OptionsPing(config)

    try:
        events.run(config.wait)
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()
