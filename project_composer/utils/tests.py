
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
