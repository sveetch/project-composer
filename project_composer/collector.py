"""
==============
Urls collector
==============

"""


class ApplicationUrlCollector:
    """
    Application urls collector is a class to inherit from an Application url class to
    implement url patterns mounting.
    """
    def __init__(self, settings=None):
        self.settings = settings

    def load_urlpatterns(self, urlpatterns):
        """
        Method to implement by Application Url classes.

        Every classes should not forget to use ``super().load_urlpatterns(urlpatterns)``
        in their ``load_urlpatterns`` method implementation, commonly at the beggining.
        """
        return urlpatterns

    def mount(self, urlpatterns):
        print("🎨 ApplicationUrlMounter Collecting urls")
        patterns = self.load_urlpatterns(urlpatterns)

        # Debug
        print()
        for item in patterns:
            print("*", item)
        print()

        return patterns
