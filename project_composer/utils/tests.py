import json


def debug_invoke(result, caplog=None):
    """
    Output important informations on Click invoke result and optionally caplog.

    It invoke command has raised an exception, raise it up.
    """
    print("=> result.output <=")
    print(result.output)
    print()

    if caplog:
        print("=> caplog.record_tuples <=")
        print(caplog.record_tuples)
        print()

    print("=> result.exception <=")
    print(result.exception)
    if result.exception is not None:
        raise result.exception


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
