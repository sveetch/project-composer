from project_composer.compose import ComposeDjangoSettings, ComposeDjangoUrls


def test_composedjangosettings_export_success(pytester, basic_structure):
    """
    Should behaves like Class composer but specifically for application settings
    modules.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = ComposeDjangoSettings({
        "name": "Sample",
        "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "basic_structure",
    })

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.export()
    ]

    assert class_names == [
        "PingSettings", "FooSettings", "BarFirstSettings", "BarSecondSettings"
    ]


def test_composedjangourls_export_success(pytester, basic_structure):
    """
    Should behaves like Class composer but specifically for application urls
    modules.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = ComposeDjangoUrls({
        "name": "Sample",
        "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "basic_structure",
    })

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.export()
    ]

    assert class_names == [
        "PongUrls", "FooUrls", "BarUrls"
    ]
