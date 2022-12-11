import inspect

from ..exceptions import ComposerConfigError
from .fields import PluginField


class BaseConfig:
    """
    Configuration class abstract.

    Attributes:
        _FIELDS (list): Required list of enabled configuration fields.
    """
    _FIELDS = []

    def __init__(self, *args, **kwargs):
        self.validate_attributes(**kwargs)
        self.install_attributes(**kwargs)

    @classmethod
    def validate_attributes(cls, **kwargs):
        """
        Validate given data against field descriptions.

        Although it's a classmethod, it is safe to call it as an instance method.

        Arguments:
            **kwargs: Fields datas.
        """
        if inspect.isclass(cls):
            klassname = cls.__name__
        else:
            klassname = cls.__class__.__name__

        for field in cls.get_fields():
            # Validate required field
            if field.required and field.name not in kwargs:
                msg = "Field '{field}' is required from '{klass}'"
                raise ComposerConfigError(msg.format(
                    field=field.name,
                    klass=klassname,
                ))

            # Validate given value against field type
            if (
                kwargs.get(field.name) is not None and
                not isinstance(kwargs.get(field.name), field.TYPE) and
                not isinstance(kwargs.get(field.name), BasePluginConfig)
            ):
                msg = "'{klass}' field '{field}' must be a '{type}' not '{wrong}'"
                raise ComposerConfigError(msg.format(
                    field=field.name,
                    type=field.TYPE.__name__,
                    klass=klassname,
                    wrong=type(kwargs.get(field.name)).__name__,
                ))

    def install_attributes(self, **kwargs):
        """
        Install defined field as object attributes with given possible values from
        kwargs.

        ``BaseConfig.validate_attributes()`` must be runned before to ensure field
        values are valid.

        Arguments:
            **kwargs: Keyword arguments for field values to set as object attribute
                value.
        """
        for field in self.get_fields():
            value = field.default
            if kwargs.get(field.name) is not None:
                value = kwargs.get(field.name)

            # Field plugin needs to build its plugin object before setting its
            # attributes
            if isinstance(field, PluginField):
                if isinstance(value, BaseConfig):
                    plugin = value
                else:
                    plugin = field.plugin()
                    plugin.install_attributes(**value)
                setattr(self, field.name, plugin)
            else:
                setattr(self, field.name, value)

    @classmethod
    def get_fields(cls):
        """
        Return model field definitions.

        Arguments:
            cls (class or object): Config class or object.

        Returns:
            list: Lists every defined field object.
        """
        return cls._FIELDS

    @classmethod
    def get_fieldnames(cls):
        """
        Return model field names.

        Arguments:
            cls (class or object): Config class or object.

        Returns:
            list: Lists every defined field name.
        """
        return [item.name for item in cls.get_fields()]

    @classmethod
    def get_fieldtypes(cls):
        """
        Return model field types.

        Arguments:
            cls (class or object): Config class or object.

        Returns:
            list: List every defined field type name.
        """
        return [item.fieldtype() for item in cls.get_fields()]

    def to_dict(self):
        """
        Dump manifest values as Python dictionnary.

        Recursively walk in ``to_dict`` method of item that are a children of
        BaseConfig.

        Returns:
            dict: Dictionnary of all field values, including the "requirements"
            ones.
        """
        content = {}

        for name in self.get_fieldnames():
            attr = getattr(self, name)
            if isinstance(attr, BasePluginConfig):
                content[name] = attr.to_dict()
            else:
                content[name] = getattr(self, name)

        return content


class BasePluginConfig(BaseConfig):
    """
    Plugin configuration abstract.
    """
    pass
