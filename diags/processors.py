from icons import (
    ApplicationStore, ApplicationRepository, Application,
    Resolver, Processor, ProcessorCaller, Project,
)


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    # Use the script filename without Python extension
    STATIC_DIR = Path("var/diags/")
    filename = STATIC_DIR / Path(__file__).stem

    # Output diagram as a PNG file with direction 'Top to Bottom'.
    with Diagram("", filename=filename, show=False, direction="TB"):

        appstore = ApplicationStore("Application store")
        repository = ApplicationRepository("Application repository")
        resolver = Resolver("Resolver")

        repository >> resolver
        resolver >> appstore
        proc_caller = ProcessorCaller("Processor caller")

        with Cluster("Processors"):
            proc_b = Processor("Processor B")
            proc_a = Processor("Processor A")

            processors = [
                proc_a,
                proc_b,
            ]

            appstore >> proc_caller
            proc_caller >> processors

            with Cluster("Part B"):
                part_b_2 = Application("App2 part B")
                part_b_1 = Application("App1 part B")

                part_b = [
                    part_b_2,
                    part_b_1,
                ]

                proc_b >> part_b

            with Cluster("Part A"):
                part_a_2 = Application("App2 part A")
                part_a_1 = Application("App1 part A")

                part_a = [
                    part_a_2,
                    part_a_1,
                ]

                proc_a >> part_a

        project = Project("Project")
        part_a >> project
        part_b >> project

    print("Built diagram at: {}".format(filename.resolve()))
