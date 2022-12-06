from icons import (
    AppNode, Application, Manifest, Resolver,
    Processor, ProcessorCaller, Project, ProjectPart,
)


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    # Use the script filename without Python extension
    STATIC_DIR = Path("var/diags/")
    filename = STATIC_DIR / Path(__file__).stem

    # Output diagram as a PNG file with direction 'Top to Bottom'.
    with Diagram("", filename=filename, show=False, direction="TB"):

        with Cluster("Application repository"):
            app_1 = Application("Application 1")
            app_3 = Application("Application 3")
            app_2 = Application("Application 2")

            repository = [
                app_1,
                app_3,
                app_2,
            ]

        manifest = Manifest("Manifest")
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

        resolver = Resolver("Resolver")
        manifest >> resolver
        resolver >> appstore

        proc_caller = ProcessorCaller("Processor caller")

        with Cluster("Processors"):
            proc_b = Processor("Processor B")
            proc_a = Processor("Processor A")

            processors = [
                proc_b,
                proc_a,
            ]

            appstore >> proc_caller
            proc_caller >> processors

            with Cluster("Part A"):
                part_a_2 = ProjectPart("App2 part A")
                part_a_1 = ProjectPart("App1 part A")

                part_a = [
                    part_a_2,
                    part_a_1,
                ]

                proc_a >> part_a

            with Cluster("Part B"):
                part_b_2 = ProjectPart("App2 part B")
                part_b_1 = ProjectPart("App1 part B")

                part_b = [
                    part_b_2,
                    part_b_1,
                ]

                proc_b >> part_b

        project = Project("Project")
        part_b >> project
        part_a >> project

    print("Built diagram at: {}".format(filename.resolve()))
