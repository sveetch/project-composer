import datetime

from pathlib import Path

from .base import ComposerBase


class TextContentComposer(ComposerBase):
    """
    Text content composer assemble all text content files from enabled Applications.
    """
    def get_template(self, template=None):
        """
        Get the base content text where to append applications requirements.

        Keyword Arguments:
            template (string or pathlib.Path): Path to file of base content to start
                output.

        Returns:
            string: Base content.
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

        if self.manifest.requirements.introduction:
            output += self.manifest.requirements.introduction.format(
                creation_date=datetime.datetime.now().isoformat(timespec="seconds"),
            )

        output += self.get_template(self.manifest.requirements.template)

        for node in self.apps:
            # Try to find application module
            module_path = self.get_module_path(node.name)
            module = self.find_app_module(module_path)

            if module and getattr(module, "__file__", None):
                # Resolve expected text content file path inside module
                source_path = (
                    Path(module.__file__).parents[0].resolve() /
                    self.manifest.requirements.source_filename
                )
                # Try to find file from application to append its content to the output
                if source_path.exists():
                    msg = "{klass} found content file at: {path}".format(
                        klass=self.__class__.__name__,
                        path=source_path,
                    )
                    self.log.debug(msg)

                    content = source_path.read_text()
                    if content.strip():
                        if self.manifest.requirements.application_divider:
                            output += self.manifest.requirements.application_divider

                        if self.manifest.requirements.application_label:
                            label = self.manifest.requirements.application_label
                            output += label.format(name=node.name)

                        output += content

                else:
                    msg = "{klass} is unable to find content file from: {path}".format(
                        klass=self.__class__.__name__,
                        path=source_path,
                    )
                    self.log.debug(msg)

        return output

    def dump(self, destination):
        """
        Write export payload to a dump file.

        Arguments:
            destination (pathlib.Path): Path object for the dump file destination.

        Returns:
            pathlib.Path: The Path object where the file has been writed.
        """
        output = self.export()
        destination.write_text(output)

        return destination
