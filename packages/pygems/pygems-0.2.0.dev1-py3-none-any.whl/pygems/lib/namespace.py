class Namespace:
    __custom_attributes: set

    def __init__(self, *args, **kwargs):
        """Create Namespace object.
        
        Accepts positional and keyword arguments. See update().

        Create Namespace object with name attribute set:
        >>> ns = Namespace({'name':'John'})
        >>> ns.name
        'John'
        """
        self.__custom_attributes = set()
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        """Update the object attributes
        
        Positional arguments are treated as dictionary:
        >>> ns = Namespace()
        >>> ns.update({'name':'John'})
        >>> ns.name
        'John'

        Keyword arguments are treated as dictionary elements:
        >>> ns = Namespace()
        >>> ns.update(name='Jane')
        >>> ns.name
        'Jane'
        
        Positional and keyword arguments can be combined:
        >>> address = {'city':'London'}
        >>> name = {'first': 'Sponge'}
        >>> ns = Namespace()
        >>> ns.update(name, address, age=23)
        >>> ns.asdict(sorted_keys=True)
        {'age': 23, 'city': 'London', 'first': 'Sponge'}
        """
        for arg in args:
            self.__dict__.update(arg)
            self.__custom_attributes.update(arg.keys())
        self.__dict__.update(kwargs)
        self.__custom_attributes.update(kwargs.keys())

    def asdict(self, sorted_keys=False):
        """Get dictionary representation of the data.
        
        Only custom attributes are exported:
        >>> ns = Namespace(name='Joan')
        >>> ns.asdict()
        {'name': 'Joan'}

        Set the `sorted_keys` parameter to True to get
        dictionary withsorted keys. Useful for docstring tests.
        >>> ns = Namespace(name='Joan', city='Arc')
        >>> ns.asdict(sorted_keys=True)
        {'city': 'Arc', 'name': 'Joan'}
        """
        if sorted_keys:
            attributes = sorted(self.__custom_attributes)
        else:
            attributes = self.__custom_attributes
        return {k:getattr(self, k) for k in attributes if hasattr(self, k) }


if __name__ == "__main__":
    import doctest
    doctest.testmod()
