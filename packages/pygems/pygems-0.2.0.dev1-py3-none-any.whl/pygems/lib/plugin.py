import typing

class BaseEventListener:
    _callback_name_template:str = 'on_{event}'

    def __init__(self, callback_name_template=None):
        if callback_name_template is not None:
            self._callback_name_template = callback_name_template

    def __call__(self, event, *args, **kwargs):
        """
        Receive event notification.

        >>> listener = BaseEventListener()
        >>> listener.on_print = lambda *args, **kwargs: print(*args)
        >>> listener('print', 'Hello', 'Ivan')
        Hello Ivan

        Unexpected events, e.g. 'write' are ignored.

        >>> listener('write', 'Bye', 'Ivan')

        Custom event handler naming temlate could be specified:
        >>> listener = BaseEventListener(callback_name_template='process_{event}')

        We define on_xyz callback which matches the default pattern, but it will be
        ignored.

        >>> listener.on_print = lambda *args, **kwargs: print('on_print:', *args)

        We also define process_xyz callback wich matches the pattern we specified during
        creation of the plugin collection. This callback will not be ignored.

        >>> listener.process_print = lambda *args, **kwargs: print('process_print:', *args)
        >>> listener('print', 'Hello', 'Ivan')
        process_print: Hello Ivan
        """
        callback_name = self._callback_name_template.format(event=event)
        callback = getattr(self, callback_name, None)
        if callback:
            callback(*args, **kwargs)

class PluginCollection:
    """Plugin Collection
    
    
    Here is example

    We define an event listener class which listens for load events. When load
    event notification is received the on_load event is called which simply 
    prints the arguments passed to it.

    >>> class EventListener(BaseEventListener):
    ...    def on_load(self, *args, **kwargs):
    ...       print(*args)

    We create a PluginCollection instance which accepts only BaseEventListener
    instances:

    >>> plugins = PluginCollection(BaseEventListener)

    We register an instance of our event listener:

    >>> _ = plugins.append(EventListener())
    
    Notifying plugins on load event will call the on_load method of our plugin
    instance:

    >>> _ = plugins.notify('load', 'myfile.txt')
    myfile.txt

    Events which are not expected are ignored. In other words event xyz is ignored
    if our event listener doesn't impmlement on_xyz method:

    >>> _ = plugins.notify('shutdown')

    Most methods return the plugin collection instance which makes it possible to 
    write code like this:

    >>> plugins = PluginCollection().append(EventListener()).notify('init')
    >>> _ = plugins.notify('load', 'bigfile.dat')
    bigfile.dat
    """
    _plugins: list
    _plugin_class: typing.Any

    def __init__(self, plugin_class=None):
        """Create and initialize PluginCollection object
        
        >>> plugins = PluginCollection()
        >>> isinstance(plugins, PluginCollection)
        True
        >>> plugins._plugins
        []
        """
        self._plugins = []
        self._plugin_class = plugin_class

    def _is_plugin_ok_to_add(self, plugin):
        assert callable(plugin), 'plugin argument should be callable'
        if self._plugin_class:
            assert isinstance(plugin, self._plugin_class), f'plugin argument should be intance of {self._plugin_class}'
        if plugin in self._plugins:
            return False
        return True

    def insert(self, *plugins):
        """Insert one or more plugins at the beginning of the collection.
        
        >>> plugins = PluginCollection().append(print)
        >>> plugins.insert(dir)._plugins
        [<built-in function dir>, <built-in function print>]

        Plugins are validated
        >>> plugins.insert(3)
        Traceback (most recent call last):
           ...
        AssertionError: plugin argument should be callable
        """
        for plugin in plugins:
            if self._is_plugin_ok_to_add(plugin):
                self._plugins.insert(0, plugin)
        return self

    def append(self, *plugins):
        """

        Appending a plugin stores it in collection:
        >>> plugins = PluginCollection()
        >>> _ = plugins.append(print)
        >>> plugins._plugins
        [<built-in function print>]

        Multiple plugins can be appended at the same time. Order is preserved:
        >>> plugins = PluginCollection()
        >>> _ = plugins.append(print, dir)
        >>> plugins._plugins
        [<built-in function print>, <built-in function dir>]
        
        Appending same plugin more than once is ignored:
        >>> plugins = PluginCollection()
        >>> _ = plugins.append(print, dir)
        >>> _ = plugins.append(print)
        >>> plugins._plugins
        [<built-in function print>, <built-in function dir>]

        Tryhing to append non-callable plugin raises error:
        >>> plugins = PluginCollection()
        >>> plugins.append(3)
        Traceback (most recent call last):
        ...
        AssertionError: plugin argument should be callable

        You can restrict type of plugins so that adding callable which is not instance
        of the given class raises assertion error. Note that instances still should be
        callable which in Python means that class implements the __call__ method:
        >>> class BasePlugin:
        ...    def __call__(self, *args, **kwargs):
        ...       print(*args, **kwargs)
        >>> plugins = PluginCollection(BasePlugin)
        >>> _ = plugins.append(BasePlugin())
        >>> _ = plugins.append(print)
        Traceback (most recent call last):
        ...
        AssertionError: plugin argument should be intance of <class 'pygems.lib.plugin.BasePlugin'>
        """
        for plugin in plugins:
            if self._is_plugin_ok_to_add(plugin):
                self._plugins.append(plugin)
        return self

    def remove(self, *plugins):
        """Remove one or more plugins
        
        >>> plugins = PluginCollection().append(print, dir)
        >>> plugins.remove(print)._plugins
        [<built-in function dir>]

        Multiple plugins could be removed at the same time:

        >>> plugins = PluginCollection().append(print, dir)
        >>> plugins.remove(print, dir)._plugins
        []
        """
        for plugin in plugins:
            self._plugins.remove(plugin)
        return self

    def notify(self, *args, **kwargs):
        """
        
        Runs all plugins from collection passing positional and keyword arguments:
        >>> plugins = PluginCollection()
        >>> _ = plugins.append(print)
        >>> _ = plugins.notify('click', 3, sep='|')
        click|3
        """
        for plugin in self._plugins:
            plugin(*args, **kwargs)
        return self

if __name__ == "__main__":
    import doctest
    doctest.testmod()
