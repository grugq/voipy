"""Ordered dictionary class.

For copyright, license, and warranty, see bottom of file.
"""

#from schevo.lib import optimize
import optimize

from types import ListType, TupleType


class odict(dict):
    """Dictionary whose keys maintain their order of membership.

    In other words, the first key added to the dictionary is the first
    key returned in the list of odict.keys(), etc.  Note that a call
    to __setitem__() for an existing key does not change the order of
    that key."""

    __slots__ = ['_keys']

    def __init__(self, seq=None):
        """dict() -> new empty dictionary.

        dict(seq) -> new dictionary initialized as if via::

            d = {}
            for k, v in seq:
                d[k] = v
        """
        self._keys = []
        if seq is None:
            dict.__init__(self)
        elif isinstance(seq, (ListType, TupleType)):
            # Lists and tuples can be iterated over again, so it's
            # safe to delegate item value assignment to the
            # superclass.
            for k, v in seq:
                if k not in self._keys:
                    self._keys.append(k)
            dict.__init__(self, seq)
        else:
            # Other sequences may only be iterated over once, so
            # initialize an empty dictionary and assign values here.
            dict.__init__(self)
            for k, v in seq:
                if k not in self._keys:
                    self[k] = v

    def __delitem__(self, key):
        """x.__delitem__(y) <==> del x[y]"""
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        for key in self._keys:
            yield key

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        itemreprs = ('%r: %r' % (key, self[key]) for key in self._keys)
        return '{' + ', '.join(itemreprs) + '}'

    def __setitem__(self, key, item):
        """x.__setitem__(i, y) <==> x[i]=y"""
        dict.__setitem__(self, key, item)
        if not hasattr(self, '_keys'):
            self._keys = [key]
        if key not in self._keys:
            self._keys.append(key)

    def append(self, key, item):
        """Alias for D[key] = item."""
        if key in self:
            raise KeyError('append(): key %r already in dictionary' % key)
        self[key] = item

    def clear(self):
        """D.clear() -> None.  Remove all items from D."""
        dict.clear(self)
        self._keys = []

    def copy(self):
        """D.copy() -> a shallow copy of D"""
        items = [(key, self[key]) for key in self._keys]
        return self.__class__(items)

    def insert(self, index, key, item):
        """Insert key:item at index."""
        if key in self:
            raise KeyError('insert(): key %r already in dictionary' % key)
        dict.__setitem__(self, key, item)
        self._keys.insert(index, key)

    def items(self):
        return [(key, self[key]) for key in self._keys]

    def iterkeys(self):
        """D.iterkeys() -> an iterator over the keys of D"""
        return iter(self)

    def iteritems(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        return ((key, self[key]) for key in self._keys)

    def itervalues(self):
        """D.itervalues() -> an iterator over the values of D"""
        return (self[key] for key in self._keys)

    def keys(self):
        """D.keys() -> list of D's keys"""
        return self._keys[:]

    def pop(self, key, *failobj):
        """D.pop(k[,d]) -> v, remove specified key and return the
        corresponding value

        If key is not found, d is returned if given, otherwise
        KeyError is raised
        """
        value = dict.pop(self, key, *failobj)
        if key in self._keys:
            self._keys.remove(key)
        return value

    def popitem(self):
        """D.popitem() -> (k, v), remove and return last (key, value)
        pair as a 2-tuple; but raise KeyError if D is empty"""
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('popitem(): dictionary is empty')
        value = self[key]
        del self[key]
        return (key, value)

    def setdefault(self, key, failobj=None):
        """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D"""
        value = dict.setdefault(self, key, failobj)
        if key not in self._keys:
            self._keys.append(key)
        return value

    def update(self, other, reorder=False):
        """Update values in this odict based on the `other` odict."""
        if not isinstance(other, odict):
            raise ValueError('other must be an odict')
        if other is self:
            raise ValueError('other cannot be the same odict')
        dict.update(self, other)
        keys = self._keys
        if not reorder:
            for key in other:
                if key not in keys:
                    keys.append(key)
        else:
            for key in other:
                if key in keys:
                    keys.remove(key)
                keys.append(key)

    def values(self):
        return [self[key] for key in self._keys]

optimize.bind_all(odict)


## # Bind the docstrings from dict to odict.
## for k, v in odict.__dict__.iteritems():
##     if k != '_keys' and hasattr(v, '__doc__') and v.__doc__ is None:
##         v.__doc__ = getattr(dict, v.__name__).__doc__


# Copyright (C) 2001-2006 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# 709 East Jackson Road
# Saint Louis, MO  63119-4241
# http://orbtech.com/
#
# This toolkit is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
