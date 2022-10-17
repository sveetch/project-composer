from project_composer.marker import EnabledApplicationMarker


class BarFirstSettings(EnabledApplicationMarker):
    BAR_FIRST_SETTING = "Bar first"


class BarSecondSettings(EnabledApplicationMarker):
    BAR_SECOND_SETTING = "Bar second"


class BarNotSettings:
    BAR_SETTING = "Bar"
