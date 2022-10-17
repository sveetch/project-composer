"""
Although these are test for base TextContentComposer, we work against
requirements behavior since it is the only TextContentComposer implemented in Manifest.
"""
from freezegun import freeze_time

from project_composer.compose import TextContentComposer


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_defaults(pytester, basic_structure):
    """
    Content text composer with defaults arguments should export application contents
    without any errors.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer({
        "name": "Sample",
        "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "basic_structure",
    })

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_intro(pytester, basic_structure):
    """
    Content text composer with an introduction.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": None,
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_without_intro(pytester, basic_structure):
    """
    Content text composer with introduction explicitely disabled.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": "",
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_custom_intro(pytester, basic_structure):
    """
    Content text composer with custom introduction given from a string.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "introduction": "# Plop intro\n",
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "# Plop intro",
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_template_string(pytester, settings,
                                                         basic_structure):
    """
    Content text composer with a template path given as a string.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    template_path = settings.fixtures_path / "requirements_template.txt"

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "template": str(template_path),
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "# Base",
        "Django",
        "ping-requirements",
        "foo-requirements",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_applabel(pytester, basic_structure):
    """
    Content text composer with an application label.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "application_label": "# {name}\n",
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "# ping",
        "ping-requirements",
        "# foo",
        "foo-requirements",
        "# bar",
        "bar-requirements"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_divider(pytester, basic_structure):
    """
    Content text composer with an application divider.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = TextContentComposer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
            "requirements": {
                "application_divider": "\n",
            }
        },
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "",
        "ping-requirements",
        "",
        "foo-requirements",
        "",
        "bar-requirements"
    ]
