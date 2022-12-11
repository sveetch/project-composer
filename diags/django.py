from diagrams.programming.framework import Django

from __init__ import get_conf, adjust_image
from icons import Composer, Manifest, PackageInstaller, Processor, ProjectPart


if __name__ == "__main__":
    from pathlib import Path

    from diagrams import Cluster, Diagram, Edge

    conf = get_conf(Path(__file__).stem)
    output_filepath = conf.pop("output_filepath")

    with Diagram("", **conf):
        manifest = Manifest("Manifest")
        composer = Composer("Composer")

        with Cluster("Processors"):
            settings_proc = Processor("DjangoSettings")
            urls_proc = Processor("DjangoUrls")
            requirements_proc = Processor("TextContent")

            processors = [
                settings_proc,
                urls_proc,
                requirements_proc
            ]

        with Cluster("Django parts"):
            settings_part = ProjectPart("Settings")
            urls_part = ProjectPart("Urls")
            requirements_part = ProjectPart("Requirements")

            parts = [
                settings_part,
                urls_part,
                requirements_part
            ]

        settings_proc >> Edge(color="darkgreen") >> settings_part
        urls_proc >> Edge(color="darkgreen") >> urls_part
        requirements_proc >> Edge(color="chocolate2") >> requirements_part

        django = Django("Django")
        pip = PackageInstaller("Pip")

        settings_part >> Edge(color="darkgreen") >> django
        urls_part >> Edge(color="darkgreen") >> django
        requirements_part >> Edge(color="chocolate2") >> pip

        manifest >> composer

        composer >> Edge(color="darkgreen") >> settings_proc
        composer >> Edge(color="darkgreen") >> urls_proc
        composer >> Edge(color="chocolate2") >> requirements_proc

    adjust_image(output_filepath.resolve())
    print("Built diagram at: {}".format(output_filepath.resolve()))
