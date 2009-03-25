#!/usr/bin/env python

from cStringIO import StringIO as StringIO
from shlex import split as _sh_split
from string import whitespace as _str_whitey



class StringBuf(object):
    # want to proxy readline()
    def __init__(self, str):
        self.__str = StringIO(str)
    def readline(self):
        # FIXME do soemthing with better checking for only eol \r\n
        return ParsingString( self.__str.readline().rstrip() )
    # XXX all of this because I can't subclass cStringIO #@!$#
    def read(self, *args): return self.__str.read(*args)
    def tell(self): return self.__str.tell()
    def seek(self, *args): return self.__str.seek(*args)
    def rewind(self): return self.__str.rewind()

def qsplit(s, sep=None, dbq='"'):
    import string

    if not len(s): return
    if not sep: sep = string.whitespace

    in_quote = False
    rl = []; word = ""
    for c in s:
        word += c
        if c in dbq:
            in_quote = not in_quote
            continue
        if c in sep:
            rl.append(word[:-1])
            word = ""
    rl.append( word )
    return rl


class ParsingString(str):
    def qsplit(self, sep=None):
        import string

        dbq = '"'
        if not len(self): return
        if not sep: sep = string.whitespace

        in_quote = False
        rl = []; word = ""
        for c in self:
            word += c
            if c in dbq:
                in_quote = not in_quote
                continue
            if c in sep:
                rl.append(word[:-1])
                word = ""
        rl.append( word )
        return [ParsingString(s) for s in rl]

        # XXX horridly broken, needs state engine
        #return [ParsingString( k.rstrip(splitchar) ) for k in _sh_split(self)]

    def splitfirst(self, sep=None): return self.split(sep, 1)
    def split(self, *args):
        return [ ParsingString(s) for s in
                super(ParsingString, self).split(*args) ]

    def findfirst(self, *args):
        ndx = -1
        for arg in args:
            for a in args:
                ndx = self.find(a)
                if ndx == -1:
                    continue
                break
        return ndx

    def indexfirst(self, *args):
        ndx = self.findfirst(args)
        if ndx == -1: raise ValueError
        return ndx
    def strip(self, *args):
        return ParsingString(super(ParsingString, self).strip(*args))
    def lstrip(self, *args):
        return ParsingString(super(ParsingString, self).lstrip(*args))
    def rstrip(self, *args):
        return ParsingString(super(ParsingString, self).rstrip(*args))

import types

class LookupList(list):
    def __init__(self, *args, **kwargs):
        self.__symtab = {}
        super(LookupList, self).__init__(*args, **kwargs)
    def _get_obj_key(self, obj):
        return obj.name
    def __getitem__(self, key):
        if key in (types.IntType, types.LongType, types.SliceType):
            return super(LookupList, self).__getitem__(key)
        return self.__symtab[ self._get_obj_key[key] ]
    def __setitem__(self, key, value):
        if key in (types.IntType, types.LongType, types.SliceType):
            # get old value for 'key'
            # attempt update
            # if successfult:
            # remove from symtab
            # update symtab
            return super(LookupList, self).__setitem__(key, value)

class SymbolicList(object):
    def __init__(self, slist=None):
        self._symtab= {}
        self._list = []

        if slist:
            self.update( slist )

    def _get_obj_name(self, obj):
        if hasattr(obj, "name"):
            return obj.name
        return ''

    def __iadd__(self, obj):
        # XXX should type.ListType checking be here??
        name = self._get_obj_name( obj )

        if name not in self._symtab:
            self._symtab[ name ] = [obj]
        else:
            self._symtab[ name ].append( obj )
        self._list.append(obj)
        return self

    def __getitem__(self, name):
        import types
        if type(name) not in types.StringTypes:
            return self._list[ name ]
        else:
            return self._symtab[ name ]
    def __setitem__(self, key, value):
        self += value
    def __iter__(self):
        return iter(self._list)
    def __len__(self):
        return len(self._list)
    def names(self):
        return self._symtab.keys()
    def iteritems(self):
        return self._symtab.iteritems()
    def update(self, other):
        for hdr in other:
            self += hdr
    # FIXME __str__()
    # FIXME __repr__()
