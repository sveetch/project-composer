from project_composer.marker import EnabledApplicationMarker


class PingSettings(EnabledApplicationMarker):
    PING_SETTING = "Ping"


class FooSettings(EnabledApplicationMarker):
    """
    Duplication of 'foo.settings.FooSettings' just to fool discovery
    """
    FOO_SETTING = "Foo ping"
