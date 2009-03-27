#!/usr/bin/env python
#
# (c) 2009, the grugq <the.grugq@gmail.com>

class Headers(object):
    def __init__(self):
        self.headers = {}
        self.raw_headers = []

    def addheader(self, key, value):
        """Add header for field key handling repeats."""
        prev = self.headers.get(key)
        if prev is None:
            self.headers[key] = value
        else:
            combined = ", ".join((prev, value))
            self.headers[key] = combined

    def addcontinue(self, key, more):
        """Add more field data from a continuation line."""
        prev = self.headers[key]
        self.headers[key] = prev + "\n " + more

    def append(self, hline):
        self.raw_headers.append(hline)

    def __len__(self):
        return len(self.headers)
    def __getitem__(self, name):
        return self.headers[name.lower()]
    def __setitem__(self, name, value):
        del self.headers[name]
        self.headers[name.lower()] = value
        text = name + ": " + value
        for line in text.split('\n'):
            self.raw_headers.append(line + '\n')
    def __delitem__(self, name):
        name = name.lower()
        if name not in self.headers:
            return
        del self.headers[name]

        name += ":"
        n = len(name)
        lst = []
        hit = 0
        for i,line in enumerate(self.raw_headers):
            if line[:n].lower() == name:
                hit = 1
            elif not line[:1].isspace():
                hit = 0
            if hit:
                lst.append(i)
        for ndx in reversed(lst):
            del self.raw_headers[i]

    def setdefault(self, name, default=""):
        lowercase = name.lower()
        if lowercase in self.headers:
            return self.headers[lowercase]
        else:
            text = name + ": " + default
            for line in text.split('\n'):
                self.headers.append(line + '\n')
            self.headers[lowercase] = default
            return default

    def has_key(self, key):
        return key in self
    def __contains__(self, name):
        return name.lower() in self.headers
    def __iter__(self):
        return iter(self.headers)
    def keys(self):
        return self.headers.keys()
    def values(self):
        return self.headers.values()
    def items(self):
        return list(self.iteritems())
    def iteritems(self):
        return self.headers.iteritems()
    def __str__(self):
        return ''.join(self.raw_headers)

_blanklines = ('\r\n', '\n')            # Optimization for islast()

def readheaders(fp):
    """Read header lines.

    Read header lines up to the entirely blank line that terminates them.
    The (normally blank) line that ends the headers is skipped, but not
    included in the returned list.  If a non-header line ends the headers,
    (which is an error), an attempt is made to backspace over it; it is
    never included in the returned list.

    The variable status is set to the empty string if all went well,
    otherwise it is an error message.  The variable headers is a
    completely uninterpreted list of lines contained in the header (so
    printing them will reproduce the header exactly as it appears in the
    file).
    """
    headers = Headers()
    status = ''
    headerseen = ""
    startofline = None

    while True:
        startofline = fp.tell()

        line = fp.readline()
        if not line:
            status = 'EOF in headers'
            break

        if headerseen and line[0] in ' \t':
            # It's a continuation line.
            headers.append(line)
            headers.addcontinue(headerseen, line.strip())
            continue

        elif iscomment(line):
            # It's a comment.  Ignore it.
            continue

        elif islast(line):
            # Note! No pushback here!  The delimiter line gets eaten.
            break

        headerseen = isheader(line)
        if headerseen:
            # It's a legal header line, save it.
            headers.append(line)
            headers.addheader(headerseen, line[len(headerseen)+1:].strip())
            continue

        else:
            # It's not a header line; throw it back and stop here.
            if not headers:
                status = 'No headers'
            else:
                status = 'Non-header line where header expected'
            # Try to undo the read.
            fp.seek(startofline)
            break
    return headers

def isheader(line):
    """Determine whether a given line is a legal header.

    This method should return the header name, suitably canonicalized.
    You may override this method in order to use Message parsing on tagged
    data in RFC 2822-like formats with special header formats.
    """
    i = line.find(':')
    if i > 0:
        return line[:i].lower()
    return None

def islast(line):
    """Determine whether a line is a legal end of RFC 2822 headers.

    You may override this method if your application wants to bend the
    rules, e.g. to strip trailing whitespace, or to recognize MH template
    separators ('--------').  For convenience (e.g. for code reading from
    sockets) a line consisting of \r\n also matches.
    """
    return line in _blanklines

def iscomment(line):
    """Determine whether a line should be skipped entirely.

    You may override this method in order to use Message parsing on tagged
    data in RFC 2822-like formats that support embedded comments or
    free-text data.
    """
    return False

def headers(buf=None):
    if buf is not None:
        fp = StringIO(buf)
        return readheaders(fp)
    return Headers()
