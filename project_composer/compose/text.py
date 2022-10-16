"""
=====================
Text content composer
=====================

"""
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

        for name in self.manifest.apps:
            # Try to find application module
            module_path = self.get_module_path(name)
            module = self.find_app_module(module_path)

            if module and getattr(module, "__file__", None):
                # Resolve expected text content file path inside module
                source_path = (
                    Path(module.__file__).parents[0].resolve() /
                    self.manifest.requirements.source_filename
                )
                # Try to find file from application to append its content to the output
                if source_path.exists():
                    self.log.debug("Found content file at: {}".format(source_path))

                    content = source_path.read_text()
                    if content.strip():
                        if self.manifest.requirements.application_divider:
                            output += self.manifest.requirements.application_divider

                        if self.manifest.requirements.application_label:
                            label = self.manifest.requirements.application_label
                            output += label.format(name=name)

                        output += content

                else:
                    msg = "Unable to find content file from: {}"
                    self.log.debug(msg.format(source_path))

        return output

    def dump(self, destination):

        output = self.export()
        destination.write_text(output)

        return destination
