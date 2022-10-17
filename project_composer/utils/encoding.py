import datetime
import json
from pathlib import Path


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Additional opiniated support for more basic object types.
    """
    def default(self, obj):
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        # Support for set to a list
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def dump_datasets(basedir, source_name, source, result, resolved_payload):
    """
    A helper function to dump source and resolving result lists in JSON files.
    """
    apps_filename = result.replace("_result", "_apps")

    source_destination = basedir / source_name
    result_destination = basedir / result
    apps_destination = basedir / apps_filename

    print("source_destination:", source_destination)
    print("result_destination:", result_destination)
    print("apps_destination:", apps_destination)

    # Write the collection source
    # print("SRC-"*30)
    # print()
    # print(source)
    source_destination.write_text(source)

    # Write the resolved collection as payload items
    result_content = json.dumps(resolved_payload, indent=4)
    # print("PAYLOAD-"*20)
    # print()
    # print(result_content)
    result_destination.write_text(result_content)

    # Write the resolved collection as just application names
    apps = json.dumps([item.get("name") for item in resolved_payload], indent=4)
    # print("APPS-"*30)
    # print()
    # print(apps)
    apps_destination.write_text(apps)

    return source_destination, result_destination, apps_destination
