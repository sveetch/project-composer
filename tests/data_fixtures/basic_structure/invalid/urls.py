from project_composer.marker import EnabledApplicationMarker

plop;plip

class InvalidSyntaxUrls(EnabledApplicationMarker):
    def load_data(self, data):
        data = super().load_data(data)
        return data + ["InvalidSyntax URL"]
