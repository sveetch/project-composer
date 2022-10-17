
class EnabledApplicationMarker:
    """
    Empty class to mark a settings class mixin as enabled to load for composition.

    This class won't never ever introduce anything else than marker attribute
    ``_ENABLED_COMPOSABLE_APPLICATION`` since the class may be herited by any kind of
    class we don't want to pollute.

    Only purpose of attribute ``_ENABLED_COMPOSABLE_APPLICATION`` is to mark it for
    inspection from composer.
    """
    _ENABLED_COMPOSABLE_APPLICATION = True
