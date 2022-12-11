
class BaseField:
    """
    Field class abstract.

    Arguments:
        name (string): The field name.

    Keyword Arguments:
        default (object): Default value when field is empty.
        required (boolean): True if the field is required to be set.
        plugin (BasePluginConfig): The plugin object where to store plugin fields.

    Attributes:
        _DEFAULT_VALUE (object): Default value to use when no one is explicitely given
            from arguments. It must fit to the field type. By default this is ``None``.
    """
    _DEFAULT_VALUE = None
    TYPE = object

    def __init__(self, name, default=None, required=False, plugin=None):
        self.name = name
        self.default = self.get_default(default)
        self.required = required
        self.plugin = plugin

    def __repr__(self):
        return "<{klass}: {name}>".format(
            klass=self.__class__.__name__,
            name=self.name
        )

    def __str__(self):
        return self.name

    def get_default(self, default=None):
        """
        Return default value.

        Keyword Arguments:
            default (object): Default value according to the field type.

        Returns:
            object: Either default value given as argument if any, else the default
                field type value.
        """
        return default or self._DEFAULT_VALUE

    def fieldtype(self):
        """
        Return the Class name that is used as the field type.
        """
        return self.__class__.__name__


class CharField(BaseField):
    """
    For simple string value.
    """
    _DEFAULT_VALUE = None
    TYPE = str


class ListField(BaseField):
    """
    For a list value.
    """
    _DEFAULT_VALUE = []
    TYPE = list


class BooleanField(BaseField):
    """
    For a boolean value.
    """
    _DEFAULT_VALUE = False
    TYPE = bool


class PluginField(BaseField):
    """
    For a plugin value.

    A plugin is a special field that include sub configuration object.
    """
    _DEFAULT_VALUE = {}
    TYPE = dict

    def __init__(self, *args, plugin, **kwargs):
        kwargs["plugin"] = plugin
        super().__init__(*args, **kwargs)
