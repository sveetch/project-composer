from ...logger import LoggerBase


class ApplicationUrlCollector(LoggerBase):
    """
    Application urls collector is a class to inherit from an Application url class to
    create url patterns collections.
    """
    def __init__(self, settings=None):
        self.settings = settings

        super().__init__()

    def load_urlpatterns(self, urlpatterns):
        """
        Method to implement by Application Url classes.

        Every classes should not forget to use ``super().load_urlpatterns(urlpatterns)``
        in their ``load_urlpatterns`` method implementation, commonly at the beggining.
        """
        return urlpatterns

    def collect(self, urlpatterns=None):
        self.log.debug("Application urls collector processing")
        urlpatterns = urlpatterns or []
        patterns = self.load_urlpatterns(urlpatterns)

        return patterns
