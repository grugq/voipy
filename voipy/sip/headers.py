#!/usr/bin/env python
# @Author:      The Grugq (grugq@hcunix.net)

from constants import headernames
import header as headerbases

class Accept(headerbases.Mime): hname="Accept"
class AcceptEncoding(headerbases.Token): hname="Accept-Encoding"
class AcceptLanguage(headerbases.Token): hname="Accept-Language"
class AlertInfo(headerbases.GenericURI): hname="Alert-Info"
class Allow(headerbases.Token): hname="Allow"
class AuthenticationInfo(headerbases.Auth): hname="Authentication-Info"
class Authorization(headerbases.Auth): hname="Authorization"
class CallID(headerbases.CallID): hname="Call-ID"
CallId = CallID
class CallInfo(headerbases.GenericURI): hname="Call-Info"
class Contact(headerbases.NameAddr): hname="Contact"
class ContentDisposition(headerbases.Token): hname="Content-Disposition"
class ContentEncoding(headerbases.Token): hname="Content-Encoding"
class ContentLanguage(headerbases.Token): hname="Content-Language"
class ContentLength(headerbases.Int): hname="Content-Length"
class ContentType(headerbases.Mime): hname="Content-Type"
class ContentTransferEncoding(headerbases.Mime): hname="Content-Transfer-Encoding"
class CSeq(headerbases.CSeq): hname = "CSeq"
class Date(headerbases.Date): hname="Date"
class ErrorInfo(headerbases.GenericURI): hname="Error-Info",
class Expires(headerbases.Int): hname="Expires"
class From(headerbases.NameAddr): hname="From"
class InReplyTo(headerbases.CallID): hname="In-Reply-To"
class MaxForwards(headerbases.Int): hname="Max-Forwards"
class MIMEVersion(headerbases.Token): hname="MIME-Version"
class MinExpires(headerbases.Int): hname="Min-Expires"
class Organization(headerbases.String): hname="Organization"
class Priority(headerbases.Token): hname="Priority"
class ProxyAuthenticate(headerbases.Auth): hname="Proxy-Authenticate"
class ProxyAuthorization(headerbases.Auth): hname="Proxy-Authorization"
class ProxyRequire(headerbases.Token): hname="Proxy-Require"
class RecordRoute(headerbases.NameAddr): hname="Record-Route"
class ReplyTo(headerbases.NameAddr): hname="Reply-To"
class Require(headerbases.Token): hname="Require"
class RetryAfter(headerbases.Int): hname="Retry-After"
class Route(headerbases.NameAddr): hname="Route"
class Server(headerbases.String): hname="Server"
class Subject(headerbases.String): hname="Subject"
class Supported(headerbases.Token): hname="Supported"
class Timestamp(headerbases.String): hname="Timestamp"
class To(headerbases.NameAddr): hname="To"
class Unsupported(headerbases.Token): hname="Unsupported"
class UserAgent(headerbases.String): hname="User-Agent"
class Via(headerbases.Via): hname="Via"
class Warning(headerbases.Warning): hname="Warning"
class WWWAuthenticate(headerbases.Auth): hname="WWW-Authenticate"

#
class GenericHeader(headerbases.Token): hname = ''

_FactoryDict = {
        "Accept" : Accept,
        "Accept-Encoding" : AcceptEncoding,
        "Accept-Language" : AcceptLanguage,
        "Alert-Info" : AlertInfo,
        "Allow" : Allow,
        "Authentication-Info" : AuthenticationInfo,
        "Authorization" : Authorization,
        "Call-ID" : CallID,
        "Call-Info" : CallInfo,
        "Contact" : Contact,
        "Content-Disposition" : ContentDisposition,
        "Content-Encoding" : ContentEncoding,
        "Content-Language" : ContentLanguage,
        "Content-Length" : ContentLength,
        "Content-Type" : ContentType,
        "CSeq" : CSeq,
        "Date" : Date,
        "Error-Info" : ErrorInfo,
        "Expires" : Expires,
        "From" : From,
        "In-Reply-To" : InReplyTo,
        "Max-Forwards" : MaxForwards,
        "MIME-Version" : MIMEVersion,
        "Min-Expires" : MinExpires,
        "Organization" : Organization,
        "Priority" : Priority,
        "Proxy-Authenticate" : ProxyAuthenticate,
        "Proxy-Authorization" : ProxyAuthorization,
        "Proxy-Require" : ProxyRequire,
        "Record-Route" : RecordRoute,
        "Reply-To" : ReplyTo,
        "Require" : Require,
        "Retry-After" : RetryAfter,
        "Route" : Route,
        "Server" : Server,
        "Subject" : Subject,
        "Supported" : Supported,
        "Timestamp" : Timestamp,
        "To" : To,
        "Unsupported" : Unsupported,
        "User-Agent" : UserAgent,
        "Via" : Via,
        "Warning" : Warning,
        "WWW-Authenticate" : WWWAuthenticate,
    }

# XXX special parsing for kwargs
#       treat kwarg as params for the primary value
#       if len(args) == 1: args[0] is a buffer
#       else:
#           args[0] == header_name, args[1:] == values

# e.g. like so:
# msg += headers.Header("to", "joe blogs <f@balh.com>", p="qqq", v="yaya")
# msg += headers.From('jill@jillsbox.com')

def Header(*args, **kwargs):
    # XXX REDO THIS!!
    # NOTE: this has to extract an hname, if the hname is known, then call
    #   the real class, let it do the parsing
    #   if the hname is unknown, set it, and build a generic object
    #   
    #   in all cases, pass hname as a seperate value
    if args:
        if len(args) == 1: # args is a buf
            vals = args[0].split(':', 1)
            if len(vals) > 1:
                hname, buf = vals
            else:
                hname, buf = vals[0], ''
        else:
            hname = args[0]
            buf = args[1]

        hdr = _FactoryDict.get( headernames.normalise( hname ), GenericHeader )
    else:
        buf = ''
        hdr = GenericHeader

    # requires updating above code, and headerbase.__init__()
    #return hdr(hname=hname, buf=buf, params=kwargs)
    return hdr(buf, params=kwargs)
