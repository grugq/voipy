#!/usr/bin/env python

import values
import headers, message, sip
from constants import methods, parameters as params
from utils import *

def Request(method, target_uri, from_uri, contact_uri):
    msg = message.Message(method=method, uri=values.NameAddr(target_uri).uri )
    msg += make_via()
    msg += headers.To( target_uri ) #uri=NameAddr(target_uri) )
    msg += headers.From( from_uri) #, tag=compute_tag(4))
    msg += headers.CallId( compute_call_id() )
    msg += headers.MaxForwards( value=70 )
    msg += headers.CSeq( sequence="1", method=method )
    msg += headers.Contact( contact_uri ) #uri=NameAddr(contact_uri) )
    msg += headers.ContentLength( value=0 )
    return msg

def Invite(target_uri, from_uri, contact_uri):
    invite = Request(methods.INVITE, target_uri, from_uri, contact_uri)
    return invite

def Register(target_uri, from_uri, contact_uri, expires=1800):
    register = Request(methods.REGISTER, target_uri, from_uri, contact_uri)
    register.cmdline.uri.user = ''
    register += headers.Expires(value=expires)
    return register

def Authorization(method, target_uri, user, passwd, authmsg):
    msg = message.Message(method=method, uri=values.NameAddr(target_uri).uri)
#    for hdr in ['to', 'from', 'call-id', 'max-forwards', 'contact',
#            'content-length', 'cseq']:
#        msg += rmsg.headers.get(hdr)
#    msg.cseq.sequence += 1
    msg += authmsg.headers['to']
    msg += authmsg.headers['from']
    msg += authmsg.headers['call-id']
    msg += authmsg.headers['max-forwards']
    msg += authmsg.headers['contact']
    msg += authmsg.headers['content-length']
    msg += authmsg.headers['cseq']
    msg.cseq.sequence += 1

    auth = None
    for authtype in ['www-authenticate', 'proxy-authenticate']:
        if authtype in authmsg.headers:
            auth = authmsg.headers[authtype]
    if auth is None:
        raise ValueError("No Authenticate header in authentication message")

    #if 'www-authenticate' in authmsg.headers['www-authenticate']:
        #auth = authmsg.headers['www-authenticate'] # also Proxy-Authenticate
    #elif 'proxy-authenticate' in authmsg.headers['proxy-authenticate']:
        #auth = authmsg.headers['proxy-authenticate']

    msg += make_authorisation(auth, method, target_uri, user, passwd)
    return msg

Authorisation=Authorization

# This is really not flexible enough... crap!, use default arg values?
def RegisterAuthorization(authmsg, user, passwd):
    # HACKHACKHACK, NameAddrHeader() should support a Uri obj argument
    target_uri = str(authmsg['to'].uri)
    from_uri = str(authmsg['from'].uri)
    if 'contact' in authmsg.headers:
        contact_uri = str(authmsg['contact'].uri)
    else:
        contact_uri = from_uri

    msg = Register(target_uri, from_uri, contact_uri)
    msg['call-id'].value = authmsg['call-id'].value
    # TODO ensure target_uri is only 'scheme:host'
    target_uri = str(msg.cmdline.uri)

    authdr = authmsg.headers.get('www-authenticate', None)
    if not authdr:
        authdr = authmsg.headers.get('proxy-authenticate', None)
    if not authdr:
        raise ValueError("No authentication headers")

    msg += make_authorisation(authdr,
            msg.cmdline.method, target_uri, user, passwd)
    return msg
RegisterAuthorisation=RegisterAuthorization
