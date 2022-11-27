import logging

import pytest

from project_composer.compose import Composer
from project_composer.contrib.django.processors import (
    DjangoSettingsProcessor, DjangoUrlsProcessor
)


def test_processor_django_basic(caplog, pytester, basic_structure):
    """
    Django classes processor should find url and settings classes as expected for
    basic structure.
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
        },
        processors=[DjangoSettingsProcessor, DjangoUrlsProcessor],
    )
    composer.resolve_collection(lazy=False)

    # Get the class names to avoid importing module classes for assertions
    settings_names = [
        item.__name__
        for item in composer.call_processor("DjangoSettingsProcessor", "export")
    ]

    assert settings_names == [
        "PingSettings",
        "FooSettings",
        "BarFirstSettings",
        "BarSecondSettings",
    ]

    urls_names = [
        item.__name__
        for item in composer.call_processor("DjangoUrlsProcessor", "export")
    ]

    assert urls_names == [
        "PongUrls", "FooUrls", "BarUrls"
    ]

    # Don't bother about logger name and log level, only messages
    assert [log[2] for log in caplog.record_tuples] == [
        "Composer found application at: basic_structure.ping",
        "Composer found application at: basic_structure.pong",
        "Composer found application at: basic_structure.foo",
        "Composer found application at: basic_structure.dummy",
        "Composer found application at: basic_structure.empty",
        "Composer found application at: basic_structure.bar",
        "DjangoSettingsProcessor found module at: basic_structure.ping.settings",
        "Composer found enabled Class at: basic_structure.ping.settings.PingSettings",
        "Composer found enabled Class at: basic_structure.ping.settings.FooSettings",
        "Composer is unable to find module: basic_structure.pong.settings",
        "DjangoSettingsProcessor found module at: basic_structure.foo.settings",
        "Composer found enabled Class at: basic_structure.foo.settings.FooSettings",
        "DjangoSettingsProcessor found module at: basic_structure.dummy.settings",
        "Composer is unable to find module: basic_structure.empty.settings",
        "DjangoSettingsProcessor found module at: basic_structure.bar.settings",
        (
            "Composer found enabled Class at: basic_structure.bar.settings."
            "BarFirstSettings"
        ),
        (
            "Composer found enabled Class at: basic_structure.bar.settings."
            "BarSecondSettings"
        ),
        "Composer is unable to find module: basic_structure.ping.urls",
        "DjangoUrlsProcessor found module at: basic_structure.pong.urls",
        "Composer found enabled Class at: basic_structure.pong.urls.PongUrls",
        "Composer found enabled Class at: basic_structure.pong.urls.FooUrls",
        "DjangoUrlsProcessor found module at: basic_structure.foo.urls",
        "Composer found enabled Class at: basic_structure.foo.urls.FooUrls",
        "DjangoUrlsProcessor found module at: basic_structure.dummy.urls",
        "Composer is unable to find module: basic_structure.empty.urls",
        "DjangoUrlsProcessor found module at: basic_structure.bar.urls",
        "Composer found enabled Class at: basic_structure.bar.urls.BarUrls"
    ]


@pytest.mark.parametrize("lazy, expected", [
    (
        False,
        [
            "FormsSettings",
            "EditorSettings",
            "FilerSettings",
            "DjangoBuiltinSettings",
            "BlogSettings",
            "RestBuiltinSettings",
            "CmsSettings",
            "CmsBlogSettings"
        ],
    ),
    (
        True,
        [
            "CmsSettings",
            "DjangoBuiltinSettings",
            "FormsSettings",
            "FilerSettings",
            "EditorSettings",
            "BlogSettings",
            "RestBuiltinSettings",
            "CmsBlogSettings",
        ],
    ),
])
def test_processor_django_advanced(caplog, pytester, advanced_structure, lazy,
                                   expected, json_debug):
    """
    Django classes processor should find url and settings classes as expected
    for advanced structure.

    Here the logs are not review but instead it matter about the lazy resolver mode.
    """
    caplog.set_level(logging.DEBUG)

    advanced_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": [
                "cms",
                "django",
                "forms",
                "filer",
                "editor",
                "blog",
                "rest",
                "cms_blog",
            ],
            "repository": "advanced_structure",
        },
        processors=[DjangoSettingsProcessor, DjangoUrlsProcessor],
    )
    composer.resolve_collection(lazy=lazy)

    # Get the class names to avoid importing module classes for assertions
    settings_names = [
        item.__name__
        for item in composer.call_processor("DjangoSettingsProcessor", "export")
    ]

    json_debug(settings_names)

    assert settings_names == expected
