from project_composer.marker import EnabledApplicationMarker


class FooUrls(EnabledApplicationMarker):
    def load_data(self, data):
        data = super().load_data(data)
        return data + ["Foo URL"]
