
class HeaderList(list):
    def __getattr__(self, name):
        if len(self) == 1:
            return getattr(self[0], name)
        raise AttributeError, "no such attribute: %s" % name
    def __setattr__(self, name, value):
        if len(self) == 1:
            return setattr(self[0], name, value)
        raise AttributeError, "Some serious problems: %s" % name

class SymbolicList(object):
    def __init__(self, *args, **kwargs):
        self._list = []
        self._map = {}
    def _get_key(self, obj):
        return obj
    def __getitem__(self, key):
        if type(key) in (int, long):
            return self._list[ key ]
        return self._map[ self._get_key(key) ]

    def __iadd__(self, obj):
        key = self._get_key( obj )
        self._map.setdefault(key, []).append( obj )
        self._list.append(obj)
        return self

    def append(self, obj):
        self += obj

    def __contains__(self, obj):
        key = self._get_key( obj )
        return key in self._map
    def __iter__(self): return iter(self._list)
    def __len__(self): return len(self._list)
    def keys(self): return self._map.keys()
    def values(self): return self._map.values()
    def get(self, key, default):
        key = self._get_key( key )
        return self._map.get( key, default )

class OrderedDict(object):
    def __init__(self, *args, **kwargs):
        self._keys = []
        self._table = {}

        if args:
            if len(args) == 1:
                if type(args[0]) == dict:
                    self._keys = args[0].keys()
                    self._table = args[0].copy()
                elif type(args[1]) in (list, tuple):
                    for i,j in args[0]:
                        self._keys.append(i)
                        self._table[i] = j
            elif len(args) == 2:
                if type(args[0]) == type(args[1]) == list:
                    self._keys = args[0]
                    for k,v in map(None, args[0], args[1]):
                        self._table[k] = v
                elif type(args[0]) == list and type(args[1]) == dict:
                    self._keys = args[0]
                    self._table = args[1].copy()
        if kwargs:
            self._keys += kwargs.keys()
            self._table.update(**kwargs)

        for k in self._keys:
            assert k in self._table, "key %r not present in table data" % k
        
        for k in self._table.keys():
            if k not in self._keys:
                self._keys.append(k)
    def __setitem__(self, key, value):
        if key not in self._table:
            self._keys.append(key)
            self._table[key] = HeaderList()
        self._table[key].append(value)
    def __getitem__(self, key):
        if type(key) == tuple:
            nd = {}
            for k in key:
                nd[k] = self._table[k]
            return self.__class__(key, nd)
        else:
            return self._table[key]
    def __delitem__(self, key):
        del self._table[key]
        self._keys.remove(key)

    def __len__(self): return len(self._keys)
    def __contains__(self, key): return key in self._keys

    def keys(self): return self._keys
    def iteritems(self):
        for k in self._keys:
            yield self._table[k]
    def values(self):
        rl = []
        for vl in [self._table[k] for k in self._keys]:
            rl.extend(vl)
        return rl
    def get(self, key, default):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

class Table(OrderedDict):
    def _get_obj_name(self, obj):
        return obj
    def __getitem__(self, obj):
        key = self._get_obj_name(obj)
        super(Table, self).__getitem__(key)
    def __setitem__(self, obj, value):
        key = self._get_obj_name(obj)
        super(Table, self).__setitem__(key, value)
    def __delitem__(self, obj):
        key = self._get_obj_name(obj)
        super(Table, self).__delitem__(key)
    def __contains__(self, name):
        key = self._get_obj_name(name)
        return super(Table, self).__contains__(key)
    def get(self, name, default):
        key = self._get_obj_name(name)
        return super(Table, self).get(key, default)
