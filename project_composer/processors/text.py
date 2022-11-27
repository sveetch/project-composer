import datetime

from pathlib import Path

from .base import ComposerProcessor
from ..exceptions import ComposerProcessorError


class TextContentProcessor(ComposerProcessor):
    """
    Text content composer assemble all text content files from enabled Applications.

    Although it has been done as a generic solution for any content files, this is
    currently tied to specific ``requirements`` plugin from manifest.
    """
    def get_template(self, template=None):
        """
        Get the base content text used to build final content.

        Keyword Arguments:
            template (string or pathlib.Path): Path to file of base content to start
                output. By default there is none.

        Returns:
            string: Base content. If no template has been given, an empty string is
            returned instead.
        """
        if template:
            template = Path(template)
            return template.read_text()

        return ""

    def export(self):
        """
        Combinate all application content files into a single content string.

        Returns:
            string: Combinated content files.
        """
        output = ""

        requirements_config = self.composer.manifest.requirements

        if requirements_config.introduction:
            output += requirements_config.introduction.format(
                creation_date=datetime.datetime.now().isoformat(timespec="seconds"),
            )

        output += self.get_template(requirements_config.template)

        for node in self.composer.apps:
            # Try to find application module
            module_path = self.composer.get_module_path(node.name)
            module = self.composer.find_app_module(module_path)

            if module and getattr(module, "__file__", None):
                # Resolve expected text content file path inside module
                source_path = (
                    Path(module.__file__).parents[0].resolve() /
                    requirements_config.source_filename
                )
                # Try to find file from application to append its content to the output
                if source_path.exists():
                    msg = "{klass} found content file at: {path}".format(
                        klass=self.__class__.__name__,
                        path=source_path,
                    )
                    self.composer.log.debug(msg)

                    content = source_path.read_text()
                    if content.strip():
                        if requirements_config.application_divider:
                            output += requirements_config.application_divider

                        if requirements_config.application_label:
                            label = requirements_config.application_label
                            output += label.format(name=node.name)

                        output += content

                else:
                    msg = "{klass} is unable to find content file from: {path}".format(
                        klass=self.__class__.__name__,
                        path=source_path,
                    )
                    self.composer.log.debug(msg)

        return output

    def dump(self, **kwargs):
        """
        Write export payload to a dump file.

        Arguments:
            destination (pathlib.Path): Path object for the dump file destination.

        Returns:
            pathlib.Path: The Path object where the file has been writed.
        """
        destination = kwargs.get("destination")
        if not destination:
            raise ComposerProcessorError("Keyword argument 'destination' is required")

        output = self.export()
        destination.write_text(output)

        return destination

    def check(self, printer=print):
        """
        Debugging check what this processor should find or match.
        """
        printer()
        printer("🧵 Processor '{}'".format(self.__class__.__name__))

        app_last = len(self.composer.apps)
        for i, node in enumerate(self.composer.apps, start=1):
            # Try to find application module
            module_path = self.composer.get_module_path(node.name)
            module = self.composer.find_app_module(module_path)

            # Display app label name
            printer(
                "X" if (i == app_last) else "T",
                node.name,
            )

            # Try to find app module file to get its path
            if module and getattr(module, "__file__", None):
                # Resolve expected text content file path inside module
                source_path = (
                    Path(module.__file__).parents[0].resolve() /
                    self.composer.manifest.requirements.source_filename
                )

                # Try to find a requirement file
                if source_path.exists():
                    content = source_path.read_text()
                    # Lists package, omits possible commentaries
                    pkgs = [
                        pkg
                        for pkg in content.strip().splitlines()
                        if not pkg.startswith("#")
                    ]
                    pkg_last = len(pkgs)
                    # Display found package lines
                    for p, pkg in enumerate(pkgs, start=1):
                        printer(
                            (
                                "O" if (i == app_last) else "I"
                            ) + (
                                "X" if (p == pkg_last) else "T"
                            ),
                            pkg,
                        )
                # There was no requirement file
                else:
                    printer(
                        "OX" if (i == app_last) else "IX",
                        "No requirement file",
                        yes_or_no=False,
                    )

        return
