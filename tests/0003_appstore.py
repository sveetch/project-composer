import json

import pytest

from project_composer.exceptions import ComposerAppStoreError
from project_composer.app_storage import AppNode, AppStore


def test_appnode_to_dict():
    """
    Should serialize AppNode object to a dictionnary using AppNode in "dependencies"
    list.
    """
    foo = AppNode("foo")
    bar = AppNode("bar", push_end=True)
    ping = AppNode("ping")
    ping.add_dependency(foo)
    pong = AppNode("pong", push_end=True)
    pong.add_dependency(foo)
    pong.add_dependency(ping)

    assert foo.to_dict() == {
        "name": "foo",
        "dependencies": [],
        "push_end": False,
    }

    assert bar.to_dict() == {
        "name": "bar",
        "dependencies": [],
        "push_end": True,
    }

    assert ping.to_dict() == {
        "name": "ping",
        "dependencies": [foo],
        "push_end": False,
    }

    assert pong.to_dict() == {
        "name": "pong",
        "dependencies": [foo, ping],
        "push_end": True,
    }


def test_appnode_to_payload():
    """
    Should serialize AppNode object to a dictionnary using name string in "dependencies"
    list.
    """
    foo = AppNode("foo")
    bar = AppNode("bar", push_end=True)
    ping = AppNode("ping")
    ping.add_dependency(foo)
    pong = AppNode("pong", push_end=True)
    pong.add_dependency(foo)
    pong.add_dependency(ping)

    assert foo.to_payload() == {
        "name": "foo",
        "dependencies": [],
        "push_end": False,
    }

    assert bar.to_payload() == {
        "name": "bar",
        "dependencies": [],
        "push_end": True,
    }

    assert ping.to_payload() == {
        "name": "ping",
        "dependencies": [foo.name],
        "push_end": False,
    }

    assert pong.to_payload() == {
        "name": "pong",
        "dependencies": [foo.name, ping.name],
        "push_end": True,
    }


def test_appstore_collection_circular_reference(settings):
    """
    Should a raise an exception for circular reference.

    TODO: Parametrize with "no_ordering" parameter
    """
    resolver = AppStore()
    source_path = (
        settings.fixtures_path / "appstore_datasets" / "circular_error_source.json"
    )

    with pytest.raises(ComposerAppStoreError) as exc_info:
        resolver.resolve(json.loads(source_path.read_text()))

    assert exc_info.value.args[0] == "Circular reference detected: ping -> bar"


def test_appstore_duplicate_names(settings):
    """
    Should a raise an exception when a same application name is not unique in
    collection.
    """
    resolver = AppStore()
    source_path = (
        settings.fixtures_path / "appstore_datasets" / "duplicate_names_source.json"
    )

    with pytest.raises(ComposerAppStoreError) as exc_info:
        resolver.resolve(json.loads(source_path.read_text()))

    assert exc_info.value.args[0] == (
        "Application 'foo' have multiple references in collection."
    )


def test_appstore_collection_unknow_dependency(settings):
    """
    Should a raise an exception for a dependency name unknow from collection.
    """
    resolver = AppStore()
    source_path = (
        settings.fixtures_path / "appstore_datasets" / "unknow_dependency.json"
    )

    with pytest.raises(ComposerAppStoreError) as exc_info:
        resolver.resolve(json.loads(source_path.read_text()))

    assert exc_info.value.args[0] == (
        "Dependency 'ping' from application 'bar' is not a registered application."
    )


def test_appstore_get_app():
    """
    Method should be able to efficiently get an app from its name in processed app list.
    """
    foo = AppNode("Foo")
    pingpong = AppNode("ping-pong")

    store = AppStore()
    store.processed_apps = [foo, pingpong]

    assert store.get_app("Nope") is None
    assert store.get_app("Foo") == foo
    assert store.get_app("ping-pong") == pingpong


def test_appstore_default_app():
    """
    If a "default_app" name is given as store argument, all app without any dependency
    should have been injected the default one during collection.
    """
    foo = AppNode("foo")
    bar = AppNode("bar")
    ping = AppNode("ping")
    ping.add_dependency(foo)
    pong = AppNode("pong")
    pong.add_dependency(foo)
    pong.add_dependency(ping)

    # print(json.dumps([
    #     foo.to_payload(),
    #     bar.to_payload(),
    #     ping.to_payload(),
    #     pong.to_payload(),
    # ], indent=4))

    store = AppStore(default_app="foo")
    store.process_collection([
        foo.to_payload(),
        bar.to_payload(),
        ping.to_payload(),
        pong.to_payload(),
    ])

    assert store.get_app("foo").to_payload() == {
        "name": "foo",
        "dependencies": [],
        "push_end": False,
    }
    assert store.get_app("bar").to_payload() == {
        "name": "bar",
        "dependencies": ["foo"],
        "push_end": False,
    }
    assert store.get_app("ping").to_payload() == {
        "name": "ping",
        "dependencies": ["foo"],
        "push_end": False,
    }
    assert store.get_app("pong").to_payload() == {
        "name": "pong",
        "dependencies": ["foo", "ping"],
        "push_end": False,
    }


def test_appstore_resolve_push_end():
    """
    Application should inherit 'push_end' value from their dependency which have it
    to True and all item that have 'push_end' to True should be pushed after the last
    app with 'push_end' to False, but resolved order should be respected during
    re-organization.
    """
    store = AppStore()
    resolved = store.resolve([
        {
            "name": "zap",
            "dependencies": [
                "ping",
            ],
        },
        {
            "name": "foo",
            "push_end": True,
        },
        {
            "name": "bar",
        },
        {
            "name": "ping",
            "dependencies": [
                "foo",
            ],
        },
        {
            "name": "pong",
            "dependencies": [
                "foo",
                "ping",
            ],
        },
        {
            "name": "twip",
        },
    ])

    # Get the resolved item as payload without any AppNode, just string names
    resolved_payload = [
        item.to_payload()
        for item in resolved
    ]

    # print()
    # print(json.dumps(resolved_payload, indent=4))
    # print()

    assert resolved_payload == [
        {
            "name": "bar",
            "dependencies": [],
            "push_end": False
        },
        {
            "name": "twip",
            "dependencies": [],
            "push_end": False
        },
        {
            "name": "foo",
            "dependencies": [],
            "push_end": True
        },
        {
            "name": "ping",
            "dependencies": [
                "foo"
            ],
            "push_end": True
        },
        {
            "name": "zap",
            "dependencies": [
                "ping"
            ],
            "push_end": True
        },
        {
            "name": "pong",
            "dependencies": [
                "foo",
                "ping"
            ],
            "push_end": True
        },
    ]


@pytest.mark.parametrize("no_ordering, expected", [
    (
        False,
        [
            "bar",
            "twip",
            "foo",
            "ping",
            "zap",
            "pong"
        ],
    ),
    (
        True,
        [
            "zap",
            "foo",
            "bar",
            "ping",
            "pong",
            "twip"
        ],
    ),
])
def test_appstore_resolve_no_ordering(no_ordering, expected):
    """
    When 'no_ordering' is enabled the resolve method should return the app list in the
    natural order from collection else this is the final resolved order.
    """
    store = AppStore(no_ordering=no_ordering)
    resolved = store.resolve([
        {
            "name": "zap",
            "dependencies": [
                "ping",
            ],
        },
        {
            "name": "foo",
            "push_end": True,
        },
        {
            "name": "bar",
        },
        {
            "name": "ping",
            "dependencies": [
                "foo",
            ],
        },
        {
            "name": "pong",
            "dependencies": [
                "foo",
                "ping",
            ],
        },
        {
            "name": "twip",
        },
    ], flat=True)

    # print()
    # print(json.dumps(resolved, indent=4))
    # print()

    assert resolved == expected


@pytest.mark.parametrize("source, expected, default_app", [
    # The most minimal
    (
        "minimal_single_source.json",
        "minimal_single_result.json",
        None,
    ),
    # A little less minimal
    (
        "minimal_multiple_source.json",
        "minimal_multiple_result.json",
        None,
    ),
    # Minimal collection with a dependency
    (
        "minimal_dependency_source.json",
        "minimal_dependency_result.json",
        None,
    ),
    # Minimal collection with no dependency and a single "push_end" sample
    (
        "minimal_nodependency_push_end_source.json",
        "minimal_nodependency_push_end_result.json",
        None,
    ),
    # Minimal collection which result to the same as before but using "default_app"
    (
        "minimal_nodependency_default-app_source.json",
        "minimal_nodependency_default-app_result.json",
        "foo",
    ),
    # Basic collection which use some dependencies and a 'push_end' inheritance sample
    (
        "basic_dependencies_push_end_source.json",
        "basic_dependencies_push_end_result.json",
        None,
    ),
    # Advanced dependency tree
    (
        "advanced_dependencies_source.json",
        "advanced_dependencies_result.json",
        None,
    ),
    # Advanced dependency tree using "default-app"
    (
        "advanced_dependencies_source.json",
        "advanced_dependencies_default-app_result.json",
        "django",
    ),
    # Advanced scenario with almost every cases
    (
        "advanced_complex_source.json",
        "advanced_complex_result.json",
        None,
    ),
    # Advanced scenario with almost every cases and using "default-app"
    (
        "advanced_complex_source.json",
        "advanced_complex_default-app_result.json",
        "django",
    ),
])
def test_appstore_dump_resolve_datasets(settings, source, expected, default_app):
    """
    Dump the source and resolved result in JSON in data_fixtures

    TODO: Parametrize with "no_ordering" parameter
    """

    source_path = settings.fixtures_path / "appstore_datasets" / source
    result_path = settings.fixtures_path / "appstore_datasets" / expected

    resolver = AppStore(default_app=default_app)

    # Translate AppNode items to payload format such as in JSON dump
    resolved_payload = [
        item.to_payload()
        for item in resolver.resolve(json.loads(source_path.read_text()))
    ]

    # from project_composer.utils.encoding import dump_datasets
    # dump_datasets(
    #    settings.fixtures_path / "appstore_datasets",
    #    source,
    #    source_path.read_text(),
    #    expected,
    #    resolved_payload
    # )

    # print()
    # print(json.dumps(resolved_payload, indent=4))
    # print()

    # print()
    # print(json.dumps([item.get("name") for item in resolved_payload], indent=4))
    # print()

    assert resolved_payload == json.loads(result_path.read_text())
