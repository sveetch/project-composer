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

    Keyword Arguments:
        application_label (string): String to start each content file block in content
            output. It expect a substitution pattern ``{name}`` where to insert the
            application name. Defaults to
            ``TextContentComposer._DEFAULT_APPLICATION_LABEL`` value.
        application_divider (string): String to add between each retrieved application
            content file in content output. Defaults to
            ``TextContentComposer._DEFAULT_APPLICATION_DIVIDER`` value.
        base_output (string or pathlib.Path): Content used as the base content
            to start output. If it is given as a Path object it will be opened to
            read and use its content.
        introduction (string): Introduction to append at the very top of content
            output. Expect a substitution pattern ``{creation_date}`` where to insert
            the current datetime in ISO format. Defaults to
            ``TextContentComposer._DEFAULT_INTRO`` value.
    """
    _DEFAULT_INTRO = (
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.\n"
        "# Written on: {creation_date}\n\n"
    )
    _DEFAULT_CONTENT_FILENAME = "source.txt"
    _DEFAULT_APPLICATION_LABEL = "# {name}\n"
    _DEFAULT_APPLICATION_DIVIDER = "\n"

    def __init__(self, *args, **kwargs):
        self.application_label = kwargs.pop("application_label",
                                            self._DEFAULT_APPLICATION_LABEL)
        self.application_divider = kwargs.pop("application_divider",
                                              self._DEFAULT_APPLICATION_DIVIDER)
        self.base_output = kwargs.pop("base_output", None)
        self.introduction = kwargs.pop("introduction", self._DEFAULT_INTRO)

        super().__init__(*args, **kwargs)

    def get_base_output(self, base_output=None):
        """
        Get the base content text where to append applications requirements.

        Keyword Arguments:
            base_output (string or pathlib.Path): Content used as the base content
                to start output. If it is given as a Path object it will be opened to
                read and use its content.

        Returns:
            string: Base content.
        """
        if base_output:
            if isinstance(base_output, str):
                return base_output
            else:
                return base_output.read_text()

        return ""

    def export(self):
        """
        Combinate all application content files into a single content string.

        Returns:
            string: Combinated content files.
        """
        output = ""

        if self.introduction:
            output += self.introduction.format(
                creation_date=datetime.datetime.now().isoformat(timespec="seconds"),
            )

        output += self.get_base_output(self.base_output)

        for name in self.apps:
            # Try to find application module
            module_path = self.get_module_path(name)
            module = self.find_app_module(module_path)

            if module and getattr(module, "__file__", None):
                # Resolve expected text content file path inside module
                source_path = (
                    Path(module.__file__).parents[0].resolve() /
                    self._DEFAULT_CONTENT_FILENAME
                )
                # Try to find file from application to append its content to the output
                if source_path.exists():
                    self.log.debug("Found content file at: {}".format(source_path))

                    content = source_path.read_text()
                    if content.strip():
                        if self.application_divider:
                            output += "\n"

                        if self.application_label:
                            output += self.application_label.format(name=name)

                        output += content

                else:
                    msg = "Unable to find content file from: {}"
                    self.log.debug(msg.format(source_path))

        return output

    def dump(self, destination):

        output = self.export()
        destination.write_text(output)

        return destination
