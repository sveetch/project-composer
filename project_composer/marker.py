
class EnabledApplicationMarker:
    """
    Application elligibility marker.

    An application part class must inherit from this to be marked as enabled to load
    for composition.

    This class implements an attribute ``_ENABLED_COMPOSABLE_APPLICATION`` used to
    validate elligibility and nothing else.

    Only purpose of attribute ``_ENABLED_COMPOSABLE_APPLICATION`` is to mark it as
    elligible for composer inspection, don't change it.

    You may however, reproduce elligibility yourself in your class with including this
    attribute, its value is not important except it must not be ``None``.
    """
    _ENABLED_COMPOSABLE_APPLICATION = True
