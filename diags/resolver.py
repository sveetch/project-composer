from icons import AppNode, Application, Manifest, Resolver


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    # Use the script filename without Python extension
    STATIC_DIR = Path("var/diags/")
    filename = STATIC_DIR / Path(__file__).stem

    # Output diagram as a PNG file with direction 'Top to Bottom'.
    with Diagram("", filename=filename, show=False, direction="TB"):

        manifest = Manifest("Manifest")
        resolver = Resolver("Resolver")

        with Cluster("Application repository"):
            app_1 = Application("Application 1")
            app_3 = Application("Application 3")
            app_2 = Application("Application 2")

            repository = [
                app_1,
                app_3,
                app_2,
            ]

        repository >> manifest

        with Cluster("Application store"):
            appnode_3 = AppNode("AppNode 3")
            appnode_2 = AppNode("AppNode 2")
            appnode_1 = AppNode("AppNode 1")

            appstore = [
                appnode_1,
                appnode_2,
                appnode_3,
            ]

        manifest >> resolver
        resolver >> appstore

    print("Built diagram at: {}".format(filename.resolve()))
