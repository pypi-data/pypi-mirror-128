class MapAsObject:
    
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, key):
        try:
            return self.wrapped[key]
        except KeyError:
            raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, key))

    def get(self, *args, **kwargs):
        return self.wrapped.get(*args, **kwargs)

    def __str__(self):
        return str(self.wrapped)
    
def as_object(wrapped_map):
    return MapAsObject(wrapped_map)
