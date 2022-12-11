from __init__ import get_conf, adjust_image
from icons import (
    ApplicationStore, ApplicationRepository, Application,
    Resolver, Processor, ProcessorCaller, Project,
)


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    conf = get_conf(Path(__file__).stem)
    output_filepath = conf.pop("output_filepath")

    with Diagram("", **conf):
        repository = ApplicationRepository("Application repository")

        with Cluster("Composer"):
            appstore = ApplicationStore("Application store")
            resolver = Resolver("Resolver")
            proc_caller = ProcessorCaller("Processor caller")

            resolver >> appstore
            appstore >> proc_caller

        repository >> resolver

        with Cluster("Processors"):
            proc_b = Processor("Processor B")
            proc_a = Processor("Processor A")

            processors = [
                proc_a,
                proc_b,
            ]

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

    adjust_image(output_filepath.resolve())
    print("Built diagram at: {}".format(output_filepath.resolve()))
