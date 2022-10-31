import logging

import pytest
from freezegun import freeze_time

from project_composer.compose import Composer
from project_composer.processors import TextContentProcessor


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_defaults(caplog, pytester, basic_structure):
    """
    Content text composer with defaults arguments should export application contents
    without any errors.
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
        processors=[TextContentProcessor],
    )
    composer.resolve_collection(lazy=False)

    output = composer.call_processor("TextContentProcessor", "export")
    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]

    # Don't bother about logger name and log level, only messages
    assert [log[2] for log in caplog.record_tuples] == [
        "Composer found application at: basic_structure.ping",
        "Composer found application at: basic_structure.pong",
        "Composer found application at: basic_structure.foo",
        "Composer found application at: basic_structure.dummy",
        "Composer found application at: basic_structure.empty",
        "Composer found application at: basic_structure.bar",
        (
            "TextContentProcessor found content file at: {}/basic_structure/ping"
            "/requirements.txt"
        ).format(pytester.path),
        (
            "TextContentProcessor is unable to find content file from: {}"
            "/basic_structure/pong/requirements.txt"
        ).format(pytester.path),
        (
            "TextContentProcessor found content file at: {}/basic_structure/foo"
            "/requirements.txt"
        ).format(pytester.path),
        (
            "TextContentProcessor is unable to find content file from: {}"
            "/basic_structure/dummy/requirements.txt"
        ).format(pytester.path),
        (
            "TextContentProcessor found content file at: {}/basic_structure/bar"
            "/requirements.txt"
        ).format(pytester.path),
    ]


@freeze_time("2012-10-15 10:00:00")
@pytest.mark.parametrize("manifest, expected", [
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": None,
            }
        },
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "ping-requirements",
            "foo-requirements",
            "bar-requirements"
        ],
    ),
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": "",
            }
        },
        [
            "ping-requirements",
            "foo-requirements",
            "bar-requirements"
        ],
    ),
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": "# Plop intro\n",
            }
        },
        [
            "# Plop intro",
            "ping-requirements",
            "foo-requirements",
            "bar-requirements"
        ],
    ),
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "template": "requirements_template.txt",
            }
        },
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "# Base",
            "Django",
            "ping-requirements",
            "foo-requirements",
            "bar-requirements"
        ],
    ),
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "application_label": "# {name}\n",
            }
        },
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "# ping",
            "ping-requirements",
            "# foo",
            "foo-requirements",
            "# bar",
            "bar-requirements"
        ],
    ),
    (
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "application_divider": "\n",
            }
        },
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "",
            "ping-requirements",
            "",
            "foo-requirements",
            "",
            "bar-requirements"
        ],
    ),
])
def test_textcontentcomposer_export_basic_variants(pytester, settings, basic_structure,
                                                   manifest, expected):
    """
    Content text processor should behave correctly depending its manifest option.

    Basic structure does not involve dependencies.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    # Augment relative template path with fixtures dir path if given
    if manifest.get("requirements", {}).get("template"):
        manifest["requirements"]["template"] = (
            settings.fixtures_path / manifest["requirements"]["template"]
        )

    composer = Composer(
        manifest,
        processors=[TextContentProcessor],
    )
    composer.resolve_collection(lazy=False)

    output = composer.call_processor("TextContentProcessor", "export")

    assert output.splitlines() == expected


@freeze_time("2012-10-15 10:00:00")
@pytest.mark.parametrize("manifest, lazy, expected", [
    (
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
        False,
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "forms-requirements",
            "editor-requirements",
            "filer-requirements",
            "blog-requirements",
            "rest-requirements",
            "cms-requirements",
            "cms_blog-requirements"
        ],
    ),
    (
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
        True,
        [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "cms-requirements",
            "forms-requirements",
            "filer-requirements",
            "editor-requirements",
            "blog-requirements",
            "rest-requirements",
            "cms_blog-requirements"
        ],
    ),
])
def test_textcontentcomposer_export_advanced(pytester, settings, advanced_structure,
                                             manifest, lazy, expected):
    """
    Content text processor should behave correctly depending its manifest option.

    Advanced structure involves dependencies so here the lazy mode is tested also.
    """
    advanced_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    # Augment relative template path with fixtures dir path if given
    if manifest.get("requirements", {}).get("template"):
        manifest["requirements"]["template"] = (
            settings.fixtures_path / manifest["requirements"]["template"]
        )

    composer = Composer(
        manifest,
        processors=[TextContentProcessor],
    )
    composer.resolve_collection(lazy=lazy)

    output = composer.call_processor("TextContentProcessor", "export")

    assert output.splitlines() == expected
