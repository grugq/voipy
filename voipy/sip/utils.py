#!/usr/bin/env python

import md5
import sip, headers
from constants import parameters as params

def compute_tag(len=8):
    from string import hexdigits
    from random import randrange
    return ''.join([hexdigits[randrange(0,15)] for i in range(len)])

def compute_call_id(len=16):
    return compute_tag(16)

def make_branch(len=10):
    return sip.BRANCH_MAGIC + compute_tag(len)

def make_via(host="localhost", branch=None):
    via = headers.Via(host=host)
    via.params['rport'] = ""
    via.params['branch'] = branch and branch or make_branch()
    return via

import md5
H = lambda data: md5.md5(data).hexdigest()
KD = lambda secret, data: H(secret + ':' + data)
A1 = lambda user, passwd, realm: user + ':' + realm + ':' + passwd
A2 = lambda method, uri: method + ':' + uri

def make_md5auth_response(user, passwd, realm, nonce, method, uri):
    return KD( H(A1(user, passwd, realm)), nonce + ':' + H(A2(method, uri)))

def make_authorisation(authdr, method, uri, user, passwd):
    if authdr.scheme.lower() != 'digest': #or authdr.algorithm.lower() != 'md5':
        raise ValueError, "Only MD5 Digest authentication is supported!"
    response = make_md5auth_response(user, passwd, authdr.realm, authdr.nonce, 
            method, uri)
    return headers.Authorization(realm=authdr.realm, nonce=authdr.nonce,
            scheme=authdr.scheme, response=response, algorithm=authdr.algorithm,
            username=user, uri=uri)
