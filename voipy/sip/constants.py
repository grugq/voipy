# methods
class methods:
    ACK = "ACK"
    BYE = "BYE"
    CANCEL = "CANCEL"
    INFO = "INFO"
    INVITE = "INVITE"
    MESSAGE = "MESSAGE"
    NOTIFY = "NOTIFY"
    OPTIONS = "OPTIONS"
    PRACK = "PRACK"
    PUBLISH = "PUBLISH"
    REFER = "REFER"
    REGISTER = "REGISTER"
    SUBSCRIBE = "SUBSCRIBE"
    UPDATE = "UPDATE"
# headers
class headernames:
    names = {
        # Long Names
        "accept" : "Accept",
        "accept-encoding" : "Accept-Encoding",
        "accept-language" : "Accept-Language",
        "alert-info" : "Alert-Info",
        "allow" : "Allow",
        "authentication-info" : "Authentication-Info",
        "authorization" : "Authorization",
        "call-id" : "Call-ID",
        "call-info" : "Call-Info",
        "contact" : "Contact",
        "content-disposition" : "Content-Disposition",
        "content-encoding" : "Content-Encoding",
        "content-language" : "Content-Language",
        "content-length" : "Content-Length",
        "content-type" : "Content-Type",
        "cseq" : "CSeq",
        "date" : "Date",
        "error-info" : "Error-Info",
        "expires" : "Expires",
        "from" : "From",
        "in-reply-to" : "In-Reply-To",
        "max-forwards" : "Max-Forwards",
        "mime-version" : "MIME-Version",
        "min-expires" : "Min-Expires",
        "organization" : "Organization",
        "priority" : "Priority",
        "proxy-authenticate" : "Proxy-Authenticate",
        "proxy-authorization" : "Proxy-Authorization",
        "proxy-require" : "Proxy-Require",
        "record-route" : "Record-Route",
        "reply-to" : "Reply-To",
        "require" : "Require",
        "retry-after" : "Retry-After",
        "route" : "Route",
        "server" : "Server",
        "subject" : "Subject",
        "supported" : "Supported",
        "timestamp" : "Timestamp",
        "to" : "To",
        "unsupported" : "Unsupported",
        "user-agent" : "User-Agent",
        "via" : "Via",
        "warning" : "Warning",
        "www-authenticate" : "WWW-Authenticate",
        # Short Names
        'i' : 'Call-ID',
        'm' : 'Contact',
        'e' : 'Content-Encoding',
        'l' : 'Content-Length',
        'c' : 'Content-Type',
        'f' : 'From',
        's' : 'Subject',
        'k' : 'Supported',
        't' : 'To',
        'v' : 'Via',
    }
    @staticmethod
    def normalise(name):
        return headernames.names.get(name.lower(), name)
    normalize = normalise # i18n support! ;)

# parameters
class parameters:
    access_type = "access-type"
    algorithm = "algorithm"
    boundary = "boundary"
    branch = "branch"
    charset = "charset"
    cnonce = "cnonce"
    comp = "comp"
    d_alg = "d-alg"
    d_qop = "d-qop"
    d_ver = "d-ver"
    directory = "directory"
    domain = "domain"
    duration = "duration"
    expiration = "expiration"
    expires = "expires"
    filename = "filename"
    from_tag = "from-tag"
    handling = "handling"
    id = "id"
    lr = "lr"
    maddr = "maddr"
    method = "method"
    micalg = "micalg"
    mobility = "mobility"
    mode = "mode"
    name = "name"
    nc = "nc"
    nonce = "nonce"
    opaque = "opaque"
    permission = "permission"
    protocol = "protocol"
    purpose = "purpose"
    q = "q"
    realm = "realm"
    reason = "reason"
    received = "received"
    response = "response"
    retry_after = "retry-after"
    rport = "rport"
    server = "server"
    site = "site"
    size = "size"
    smime_type = "smime-type"
    stale = "stale"
    tag = "tag"
    to_tag = "to-tag"
    transport = "transport"
    ttl = "ttl"
    uri = "uri"
    user = "user"
    username = "username"
# codes
class responsecodes:
    informational  =  {
    "100"  :  "Trying",
    "180"  :  "Ringing",
    "181"  :  "Call Is Being Forwarded",
    "182"  :  "Queued",
    "183"  :  "Session Progress",
    }

    success  =  {
    "200"  :  "OK",
    "202"  :  "Accepted",
    }

    redirection  =  {
    "300"  :  "Multiple Choices",
    "301"  :  "Moved Permanently",
    "302"  :  "Moved Temporarily",
    "305"  :  "Use Proxy",
    "380"  :  "Alternative Service",
    }

    client_error  =  {
    "400"  :  "Bad Request",
    "401"  :  "Unauthorized",
    "402"  :  "Payment Required",
    "403"  :  "Forbidden",
    "404"  :  "Not Found",
    "405"  :  "Method Not Allowed",
    "406"  :  "Not Acceptable",
    "407"  :  "Proxy Authentication Required",
    "408"  :  "Request Timeout",
    "410"  :  "Gone",
    "413"  :  "Request Entity Too Large",
    "414"  :  "Request-URI Too Large",
    "415"  :  "Unsupported Media Type",
    "416"  :  "Unsupported URI Scheme",
    "420"  :  "Bad Extension",
    "421"  :  "Extension Required",
    "423"  :  "Interval Too Brief",
    "480"  :  "Temporarily not available",
    "481"  :  "Call Leg/Transaction Does Not Exist",
    "482"  :  "Loop Detected",
    "483"  :  "Too Many Hops",
    "484"  :  "Address Incomplete",
    "485"  :  "Ambiguous",
    "486"  :  "Busy Here",
    "487"  :  "Request Terminated",
    "488"  :  "Not Acceptable Here",
    "491"  :  "Request Pending",
    "493"  :  "Undecipherable",
    }

    server_error  =  {
    "500"  :  "Internal Server Error",
    "501"  :  "Not Implemented",
    "502"  :  "Bad Gateway",
    "503"  :  "Service Unavailable",
    "504"  :  "Server Time-out",
    "505"  :  "SIP Version not supported",
    "513"  :  "Message Too Large",
    }

    global_failure  =  {
    "600"  :  "Busy Everywhere",
    "603"  :  "Decline",
    "604"  :  "Does not exist anywhere",
    "606"  :  "Not Acceptable",
    }

    all =  dict( 
        informational.items() + \
        success.items() + \
        redirection.items() + \
        client_error.items() + \
        server_error.items() + \
        global_failure.items()
    )

    @staticmethod
    def is_informational(code): code=int(code); return code >= 100 and code <= 199
    @staticmethod
    def is_success(code): code=int(code); return code >= 200 and code <= 299
    @staticmethod
    def is_redirection(code): code=int(code); return code >= 300 and code <= 399
    @staticmethod
    def is_client_error(code): code=int(code); return code >= 400 and code <= 499
    @staticmethod
    def is_server_error(code): code=int(code); return code >= 500 and code <= 599
    @staticmethod
    def is_global_failure(code): code=int(code); return code >= 600 and code <= 699

    @staticmethod
    def response_by_code(code):
        return responsecodes.all[str(code)]
