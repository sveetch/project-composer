from project_composer.marker import EnabledApplicationMarker


class BarUrls(EnabledApplicationMarker):
    def load_data(self, data):
        data = super().load_data(data)
        return data + ["Bar URL"]
