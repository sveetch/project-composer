
def project_settings(composer, base_classes=None, name=None):
    """
    Build composed settings class for given composer.

    Arguments:
        composer (project_composer.compose.Composer): Composer instance.

    Keyword Arguments:
        base_classes (list): A list of base classes inheritage to build the settings
            class. Default to empty list.
        name (string): Class name to set. Default to ``ComposedProjectSettings``.

    Returns:
        object: Composed settings class.
    """
    base_classes = base_classes or []
    name = name or "ComposedProjectSettings"

    # Search for all enabled classes
    classes = composer.call_processor("DjangoSettingsProcessor", "export")

    # Reverse the list since Python class inheritance order start from the last
    # statement to the first
    classes.reverse()

    # Return built settings class from composed settings classes
    return type(name, tuple(classes + base_classes), {})


def project_urls(composer, settings, base_classes=None, name=None):
    """
    Build composed urls collector class for given composer.

    Arguments:
        composer (project_composer.compose.Composer): Composer instance.
        settings (django.conf.settings): Django settings to give to the collector.

    Keyword Arguments:
        base_classes (list): A list of base classes inheritage to build the settings
            class. Default to empty list.
        name (string): Class name to set. Default to ``ComposedProjectSettings``.

    Returns:
        list: List of collected url patterns (like ``django.urls.path`` or
        ``django.urls.re_path``) from all application urls classes.
    """
    base_classes = base_classes or []
    name = name or "ComposedProjectUrls"

    # Search for all enabled classes
    classes = composer.call_processor("DjangoUrlsProcessor", "export")

    # Build Urls class from composed urls
    composed = type(name, tuple(classes + base_classes), {})

    # Collect and return applications urls
    mounter = composed(settings)
    return mounter.collect()
