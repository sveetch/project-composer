import logging

from project_composer.compose import Composer
from project_composer.processors import TextContentProcessor
from project_composer.contrib.django.processors import (
    DjangoSettingsProcessor, DjangoUrlsProcessor
)


def test_check_basic(caplog, capsys, pytester, basic_structure):
    """
    Composer check should output all expected debugging informations.
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "nope", "dummy", "empty", "bar"],
            "repository": "basic_structure",
        },
        processors=[DjangoSettingsProcessor, DjangoUrlsProcessor, TextContentProcessor],
    )
    composer.check(lazy=False)

    captured = capsys.readouterr()

    assert captured.out.splitlines() == [
        "👷 Checking composer",
        "",
        "📄 Manifest",
        "├── Name: Sample",
        "├── Repository: basic_structure",
        "└── Collection:",
        "    ├── ping",
        "    ├── nope",
        "    ├── dummy",
        "    ├── empty",
        "    └── bar",
        "",
        "🌐 Repository directory",
        "└─✔ {}/basic_structure".format(pytester.path),
        "    ├─✔ {}/basic_structure/ping".format(pytester.path),
        "    ├─✖ {}/basic_structure/nope".format(pytester.path),
        "    ├─✔ {}/basic_structure/dummy".format(pytester.path),
        "    ├─✔ {}/basic_structure/empty".format(pytester.path),
        "    └─✔ {}/basic_structure/bar".format(pytester.path),
        "",
        "🗃️ Resolved applications",
        "├── ping",
        "│   ├── Push end: False",
        "│   └── No dependency",
        "├── dummy",
        "│   ├── Push end: False",
        "│   └── No dependency",
        "├── empty",
        "│   ├── Push end: False",
        "│   └── No dependency",
        "└── bar",
        "    ├── Push end: False",
        "    └── No dependency",
        "",
        "🧵 Processor 'DjangoSettingsProcessor'",
        "├── ping",
        "│   ├── PingSettings",
        "│   └── FooSettings",
        "├── dummy",
        "├── empty",
        "└── bar",
        "    ├── BarFirstSettings",
        "    └── BarSecondSettings",
        "",
        "🧵 Processor 'DjangoUrlsProcessor'",
        "├── ping",
        "├── dummy",
        "├── empty",
        "└── bar",
        "    └── BarUrls",
        "",
        "🧵 Processor 'TextContentProcessor'",
        "├── ping",
        "│   └── ping-requirements",
        "├── dummy",
        "│   └─✖ No requirement file",
        "├── empty",
        "└── bar",
        "    └── bar-requirements",
    ]
