from __init__ import get_conf, adjust_image
from icons import AppNode, Application, Manifest, Resolver


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    conf = get_conf(Path(__file__).stem)
    output_filepath = conf.pop("output_filepath")

    with Diagram("", **conf) as diag:
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
            appnode_1 = AppNode("AppNode 1")
            appnode_2 = AppNode("AppNode 2")
            appnode_3 = AppNode("AppNode 3")

            appstore = [
                appnode_1,
                appnode_2,
                appnode_3,
            ]

        manifest >> resolver
        resolver >> appstore

    adjust_image(output_filepath.resolve())
    print("Built diagram at: {}".format(output_filepath.resolve()))
