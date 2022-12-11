"""
This contains dummy proxy objects to the right icons since it currently use GCP icons
but is awaiting for a better and more accurate icon set.
"""
from diagrams.gcp.analytics import Composer as GCPComposer, Pubsub
from diagrams.gcp.compute import GKEOnPrem, ComputeEngine, GPU
from diagrams.gcp.database import Memorystore
from diagrams.gcp.devtools import ContainerRegistry, IdePlugins, SDK
from diagrams.gcp.ml import AdvancedSolutionsLab, AIHub
from diagrams.gcp.storage import Filestore


class Manifest(Filestore):
    pass


class ApplicationStore(AIHub):
    pass


class ApplicationRepository(ContainerRegistry):
    pass


class AppNode(SDK):
    pass


class Application(IdePlugins):
    pass


class Composer(GCPComposer):
    pass


class Resolver(Pubsub):
    pass


class ProcessorCaller(Memorystore):
    pass


class Processor(ComputeEngine):
    pass


class ProjectPart(GPU):
    pass


class PackageInstaller(GKEOnPrem):
    pass


class Project(AdvancedSolutionsLab):
    pass


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram

    from __init__ import get_conf, adjust_image

    conf = get_conf(Path(__file__).stem)
    output_filepath = conf.pop("output_filepath")

    with Diagram("", **conf):
        with Cluster("GCP set"):
            with Cluster("Sources of truth"):
                manifest = Manifest("Manifest")

            with Cluster("Applications"):
                appstore = ApplicationStore("Application store")
                repository = ApplicationRepository("Application repository")
                appnode = AppNode("AppNode")
                application = Application("Application")

            with Cluster("Composer mechanics"):
                composer = Composer("Composer")
                resolver = Resolver("Resolver")
                proc_caller = ProcessorCaller("Processor caller")

            with Cluster("Processors"):
                processor = Processor("Processor")
                project_part = ProjectPart("Project part")

            with Cluster("Consumers"):
                packager_installer = PackageInstaller("Package installer")
                project = Project("Project")

    adjust_image(output_filepath.resolve())
    print("Built diagram at: {}".format(output_filepath.resolve()))
