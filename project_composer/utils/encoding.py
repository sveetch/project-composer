import datetime
import json
from pathlib import Path

from ..app_storage import AppNode


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Extended JSON encoder to support more basic and internal object types.

    Sample usage: ::

        import json
        json.dumps({}, indent=4, cls=ExtendedJsonEncoder)

    """
    def default(self, obj):
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        # Support for set to a list
        if isinstance(obj, set):
            return list(obj)
        # Support for AppNode to a dict
        if isinstance(obj, AppNode):
            return obj.to_payload()
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
