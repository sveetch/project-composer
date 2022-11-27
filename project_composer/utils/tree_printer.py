
class TreePrinter:
    """
    Shortcut to make tree row output.

    This is useful to display a tree without a real tree implementation.

    It allows to display tree rows each one after one. However this technique is not
    very smart and so you need to give it a pattern that it will correctly pad and
    translate to the right glyphs.

    Usage example: ::

        treeprint = TreePrinter()

        treeprint("Plop")
        >>>Plop
        treeprint("T", "Plap")
        >>>├──Plap
        treeprint("T", "Plip")
        >>>├──Plip
        treeprint("IT", "Ping")
        >>>│  ├──Ping
        treeprint("IIX", "Zip")
        >>>│  │  └──Zip
        treeprint("IIOT", "Zap")
        >>>│  │     └──Zap
        treeprint("IIOIT", "Yyyy")
        >>>│  │        ├──Yyyy
        treeprint("IIOIX", "Zzzz")
        >>>│  │        └──Zzzz
        treeprint("IIOX", "Zup")
        >>>│  │     └──Zup
        treeprint("IX", "Pong")
        >>>│  └──Pong
        treeprint("X", "Plop")
        >>>└──Plop

    """
    TEE_CHAR = "├"
    ELBOW_CHAR = "└"
    LINE_CHAR = "── "
    YESLINE_CHAR = "─✔ "
    NOLINE_CHAR = "─✖ "
    PIPE_CHAR = "│"
    VOID_CHAR = " "

    def __init__(self, printable=False):
        self.store = {}
        self.current_level = 0
        self.spectrum = ""
        self.printable = printable

    def __call__(self, *args, **kwargs):
        if self.printable:
            print(self.build(*args, **kwargs))
        else:
            return self.build(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        Build the ascii row for given content.

        Arguments:
            *args: Either just the content without pattern. Or the pattern then the
                content.

        Returns:
            string: The ascii row glyphs followed by given content.
        """
        if len(args) == 0:
            return ""
        elif len(args) > 1:
            pattern = args[0]
            content = args[1]
        else:
            pattern = ""
            content = args[0]

        yes_or_no = kwargs.get("yes_or_no", None)

        # Enforce string
        content = str(content)

        return self.get_indent(pattern, yes_or_no=yes_or_no) + content

    def get_indent(self, pattern, yes_or_no=None):
        """
        Convert a pattern to an ascii tree row

        * "T" is for an intersection part, when the current item have sibling;
        * "X" is for an end part, when current item have no sibling;
        * "O" is for a void part, when there is parent level without sibling;
        * "I" is for a pipe part, when there is parent with sibling;

        Arguments:
            pattern (string): A pattern composed of letters used to determined the
                ascii representation to append to output.

        Keyword Arguments:
            yes_or_no (boolean): If True use YESLINE_CHAR, if false use NOLINE_CHAR and
                finally if None (default) use LINE_CHAR for intersection and end parts.

        Returns:
            string: Ascii representation of pattern.
        """
        output = ""

        line_char = self.LINE_CHAR
        if yes_or_no is True:
            line_char = self.YESLINE_CHAR
        elif yes_or_no is False:
            line_char = self.NOLINE_CHAR

        if pattern:
            for item in pattern.upper():
                if item == "T":
                    output += self.TEE_CHAR + line_char
                elif item == "I":
                    output += self.PIPE_CHAR + (" " * len(self.LINE_CHAR))
                elif item == "O":
                    output += self.VOID_CHAR + (" " * len(self.LINE_CHAR))
                elif item == "X":
                    output += self.ELBOW_CHAR + line_char

        return output
