import pytest

from project_composer.exceptions import ComposerConfigError
from project_composer.manifest.base import BaseConfig, BasePluginConfig
from project_composer.manifest.fields import CharField, ListField, PluginField


def test_get_fields():
    """
    Getting fields from a BaseConfig should work both as class method and instance
    method.
    """
    class SubConfig(BasePluginConfig):
        _FIELDS = []

    name_field = CharField("name")
    apps_field = ListField("collection")
    contents_field = PluginField("contents", plugin=BasePluginConfig)

    class BasicConfig(BaseConfig):
        _FIELDS = [name_field, apps_field, contents_field]

        def __init__(self, *args, **kwargs):
            # Disable initial initialize
            pass

    # Directly as class methods
    assert BasicConfig.get_fields() == [name_field, apps_field, contents_field]
    assert BasicConfig.get_fieldnames() == ["name", "collection", "contents"]
    assert BasicConfig.get_fieldtypes() == ["CharField", "ListField", "PluginField"]

    # As instance method
    manifest = BasicConfig("name", [])
    assert manifest.get_fields() == [name_field, apps_field, contents_field]
    assert manifest.get_fieldnames() == ["name", "collection", "contents"]
    assert manifest.get_fieldtypes() == ["CharField", "ListField", "PluginField"]


def test_validate_attributes():
    """
    Given fields should be correctly validated and raise error if not.
    """
    category_field = CharField("category", default="Filou")

    class SubConfig(BasePluginConfig):
        _FIELDS = [category_field]

    name_field = CharField("name", required=True)
    apps_field = ListField("collection")
    contents_field = PluginField("contents", plugin=SubConfig)

    class BasicConfig(BaseConfig):
        _FIELDS = [name_field, apps_field, contents_field]

        def __init__(self, *args, **kwargs):
            # Disable initial initialize
            pass

    # Config without the required field
    manifest = BasicConfig()
    with pytest.raises(ComposerConfigError) as exc_info:
        manifest.validate_attributes()
    assert exc_info.value.args[0] == "Field 'name' is required from 'BasicConfig'"

    # Config invalid value type for a field
    manifest = BasicConfig()
    with pytest.raises(ComposerConfigError) as exc_info:
        manifest.validate_attributes(name="foo", contents="bar")
    assert exc_info.value.args[0] == (
        "'BasicConfig' field 'contents' must be a 'dict' not 'str'"
    )


def test_install_attributes():
    """
    Class fields should be correctly installed as object attributes depending their
    parameters and given kwargs.
    """
    category_field = CharField("category", default="Filou")

    class SubConfig(BasePluginConfig):
        _FIELDS = [category_field]

    name_field = CharField("name", required=True)
    apps_field = ListField("collection")
    contents_field = PluginField("contents", plugin=SubConfig)

    class BasicConfig(BaseConfig):
        _FIELDS = [name_field, apps_field, contents_field]

        def __init__(self, *args, **kwargs):
            # Disable initial initialize
            pass

    # Basic config only with required field
    manifest = BasicConfig()
    manifest.install_attributes(name="basic")
    assert manifest.name == "basic"
    assert manifest.collection == []
    assert manifest.contents.category == "Filou"

    manifest = BasicConfig()
    manifest.install_attributes(
        name="foo",
        collection=["plop", "plip"],
        contents={"pi": "po", "category": "zen"}
    )
    assert manifest.name == "foo"
    assert manifest.collection == ["plop", "plip"]
    assert manifest.contents.category == "zen"


def test_install_to_dict(json_debug):
    """
    Class fields should be correctly installed as object attributes depending their
    parameters and given kwargs.
    """
    class SubConfig(BasePluginConfig):
        _FIELDS = [CharField("category", default="Filou")]

    class BasicConfig(BaseConfig):
        _FIELDS = [
            CharField("name", required=True),
            ListField("collection"),
            PluginField("contents", plugin=SubConfig),
        ]

    manifest = BasicConfig(
        name="foo",
        collection=["plop", "plip"],
        contents={"pi": "po", "category": "zen"}
    )

    assert manifest.to_dict() == {
        "name": "foo",
        "collection": [
            "plop",
            "plip"
        ],
        "contents": {
            "category": "zen"
        }
    }
