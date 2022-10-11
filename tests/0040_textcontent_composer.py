"""
Although these are test for base TextContentComposer, we work against
requirements behavior since it is the only TextContentComposer implemented in Manifest.
"""
from freezegun import freeze_time

from project_composer.compose import TextContentComposer


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_defaults():
    """
    Content text composer with defaults arguments should export application contents
    without any errors.
    """
    composer = TextContentComposer({
        "name": "Sample",
        "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "tests.data_fixtures.apps_structure",
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
def test_textcontentcomposer_export_with_intro():
    """
    Content text composer with an introduction.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
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
def test_textcontentcomposer_export_without_intro():
    """
    Content text composer with introduction explicitely disabled.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
            "requirements": {
                "introduction": False,
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
def test_textcontentcomposer_export_custom_intro():
    """
    Content text composer with custom introduction given from a string.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
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
def test_textcontentcomposer_export_with_template_string(settings):
    """
    Content text composer with a template path given as a string.
    """
    template_path = settings.fixtures_path / "requirements_template.txt"

    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
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
def test_textcontentcomposer_export_with_template_pathobject(settings):
    """
    Content text composer with a template path given as a Path object.
    """
    template_path = settings.fixtures_path / "requirements_template.txt"

    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
            "requirements": {
                "template": template_path,
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
def test_textcontentcomposer_export_with_applabel():
    """
    Content text composer with an application label.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
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
def test_textcontentcomposer_export_with_divider():
    """
    Content text composer with an application divider.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "tests.data_fixtures.apps_structure",
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
