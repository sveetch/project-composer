from project_composer.marker import EnabledApplicationMarker


class PongUrls(EnabledApplicationMarker):
    def load_data(self, data):
        data = super().load_data(data)
        return data + ["Pong URL"]


class FooUrls(EnabledApplicationMarker):
    """
    Duplication of 'foo.urls.FooUrls' just to fool discovery
    """
    def load_data(self, data):
        data = super().load_data(data)
        return data + ["Foo pong URL"]
