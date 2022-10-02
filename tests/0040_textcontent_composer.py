from freezegun import freeze_time

from project_composer.compose import TextContentComposer


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_defaults():
    """
    Content text composer with defaults arguments should export application contents
    without any errors.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure",
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "",
        "# ping",
        "ping-source",
        "",
        "# foo",
        "foo-requirements",
        "",
        "# bar",
        "bar-source"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_nointro():
    """
    Content text composer without introduction.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure",
        introduction=None,
    )

    output = composer.export()

    assert output.splitlines() == [
        "",
        "# ping",
        "ping-source",
        "",
        "# foo",
        "foo-requirements",
        "",
        "# bar",
        "bar-source"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_base_string():
    """
    Content text composer with a base content given as a string.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure",
        base_output="base",
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "base"
        "",
        "# ping",
        "ping-source",
        "",
        "# foo",
        "foo-requirements",
        "",
        "# bar",
        "bar-source"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_with_base_file(settings):
    """
    Content text composer with a base content given as a file.
    """
    base_output_path = settings.fixtures_path / "requirements_template.txt"

    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure",
        base_output=base_output_path,
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "# Base",
        "Django",
        "",
        "# ping",
        "ping-source",
        "",
        "# foo",
        "foo-requirements",
        "",
        "# bar",
        "bar-source"
    ]


@freeze_time("2012-10-15 10:00:00")
def test_textcontentcomposer_export_nolabel_nodivider():
    """
    Content text composer without application label and divider.
    """
    composer = TextContentComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure",
        application_label=None,
        application_divider=None,
    )

    output = composer.export()

    assert output.splitlines() == [
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
        "# Written on: 2012-10-15T10:00:00",
        "",
        "ping-source",
        "foo-requirements",
        "bar-source"
    ]
