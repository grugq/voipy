#!/usr/bin/env python

import copy
import headers, code, message
from codes import responsecodes

# should be a copy from a request, e.g. if kwargs['request']: ...
def Response(status, reason, to_uri, from_uri, contact_uri):
    reason = responsecodes.all.get(str(status).strip(), "No reason")
    response = message.Message(status, reason)

    return response

def ResponseTo(status, reason, request):
    reason = responsecodes.all.get(str(status), "No reason")
    response = message.Message(status, reason)

    for hdr in request.headers.iter_items():
        response += copy.copy(hdr)
    return response
