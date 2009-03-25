#!/usr/bin/env python

from lib import odict

class VoIPyObject(object):
    def __init__(self, buf=None, **kwargs):
        if buf:
            self.parse(buf)
        if kwargs:
            self._loadargs(**kwargs)
    def parse(self, buf):
        pass
    def _loadargs(self, **kwargs):
        pass
    def __str__(self):
        return self.pack()
    def __repr__(self):
        if not hasattr(self, '__slots__'):
            return super(VoIPyObject, self).__repr__()
        return '<%s %s>' % (self.__class__.__name__, ', '.join(['%s=%r' %
                (k,getattr(self,k)) for k in self.__slots__]))

class HeaderList(list):
    def __init__(self, key, container, *args, **kwargs):
        super(HeaderList, self).__init__(*args, **kwargs)
        self.__dict__['_container'] = container
        self.__dict__['_key'] = key
    def __delitem__(self, ndx):
        super(HeaderList, self).__delitem__(ndx)
        if not len(self):
            del self._container[self._key]
    def __setitem__(self, ndx, value):
        value = self._container._munge_value(value)
        return super(HeaderList, self).__setitem__(ndx, value)
    def append(self, value):
        value = self._container._munge_value(value)
        super(HeaderList, self).append(value)
    def __contains__(self, value):
        value = self._container._munge_value(value)
        return super(HeaderList, self).__contains__(value)
    def __getattr__(self, name):
        if len(self):
            return getattr(self[0], name)
        raise AttributeError, "No such attribute: '%r'" % name
    def __setattr__(self, name, value):
        if len(self):
            return setattr(self[0], name, value)
        raise AttributeError, "No entries to modify '%r'" % name

class HeaderTable(odict.odict):
    def __init__(self, *args, **kwargs):
        super(HeaderTable, self).__init__(*args, **kwargs)
        self.__initialized = True
    def _munge_value(self, key, value):
        return value
    def _get_key(self, key):
        return key
    def __delitem__(self, key):
        key = self._get_key(key)
        return super(HeaderTable, self).__delitem__(key)
    def __setitem__(self, key, value):
        key = self._get_key(key)
        if key not in self:
            super(HeaderTable, self).__setitem__(key, HeaderList(key, self))
        super(HeaderTable, self).__getitem__(key).append(value)
    def __getitem__(self, key):
        key = self._get_key(key)
        return super(HeaderTable, self).__getitem__(key)
    def __contains__(self, key):
        key = self._get_key(key)
        return super(HeaderTable, self).__contains__(key)
    def get(self, key, default=None):
        key = self._get_key(key)
        return super(HeaderTable, self).get(key, default)
    def __iadd__(self, other):
        if type(other) in (list, tuple):
            for obj in other:
                self += obj
        elif type(other) == dict:
            for k,v in dict.iteritems():
                self[k] = v
        else:
            value = self._munge_value(other)
            key = self._get_key(value)
            self.__setitem__(key, value)
        return self
    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError, "No such key '%r'" % self._get_key(key)
    def __setattr__(self, key, value):
        if '_HeaderTable__initialized' not in self.__dict__ \
           or key in self.__dict__:
            super(HeaderTable, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)
    def __iter__(self):
        for vlist in self.values():
            for value in vlist:
                yield value
#    def __repr__(self):
#        return '{%s}' % ', '.join(['%s: %r'%(k,v) for k,v in self.items()])




class CmdLine(VoIPyObject):
    def _repr(self, members):
        return '<%s %s>' % (self.__class__.__name__, ', '.join(['%s=%r' % \
                                    (k,getattr(self,k)) for k in members]))
class Header(VoIPyObject): pass

class Message(VoIPyObject):
    __slots__ = ['cmdline', 'headers', 'body']
    class Factory:
        @staticmethod
        def cmdline(*args, **kwargs): raise UnimplementedError
        @staticmethod
        def headertable(*args, **kwargs): raise UnimplementedError
        @staticmethod
        def header(*args, **kwargs): raise UnimplementedError
        @staticmethod
        def body(*args, **kwargs): raise UnimplementedError

    def __init__(self, buf=None, **kwargs):
        self.cmdline = self.Factory.cmdline()
        self.headers = self.Factory.headertable()
        self.body = self.Factory.body()

        super(Message, self).__init__(buf, **kwargs)
