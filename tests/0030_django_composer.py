from project_composer.compose import ComposeDjangoSettings, ComposeDjangoUrls


def test_composedjangosettings_export_success():
    """
    Should behaves like Class composer but specifically for application settings
    modules.
    """
    composer = ComposeDjangoSettings({
        "name": "Sample",
        "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "tests.data_fixtures.apps_structure",
    })

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.export()
    ]

    assert class_names == [
        "PingSettings", "FooSettings", "BarFirstSettings", "BarSecondSettings"
    ]


def test_composedjangourls_export_success():
    """
    Should behaves like Class composer but specifically for application urls
    modules.
    """
    composer = ComposeDjangoUrls({
        "name": "Sample",
        "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "tests.data_fixtures.apps_structure",
    })

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.export()
    ]

    assert class_names == [
        "PongUrls", "FooUrls", "BarUrls"
    ]
