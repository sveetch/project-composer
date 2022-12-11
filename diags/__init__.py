"""
Default values for Diagram args and kwargs
"""
from pathlib import Path

from PIL import Image


STATIC_DIR = Path("../docs/_static/")


def get_conf(filepath, horizontal=True, extra=None):
    """
    Build options for 'diagrams.Diagrams'.

    Default option configuration build a PNG image with transparent background where
    items are aligned from left to the right.

    Arguments:
        filepath (pathlib.Path): Path object for output file destination.

    Keyword Arguments:
        horizontal (boolean): If True, the main direction "left to right" is
            used. If False, the main direction "top to bottom" is used. Default to
            True. Keep in mind that graphviz ordering is special and you may probably
            not retrieve the same item order from horizontal to vertical direction.
        extra (dict): A dictionnary to override items from built options dict.

    Returns:
        dict: Dictionnary of Diagrams options plus additional item 'output_filepath'.
        You will have to pop this additional item before giving options to Diagrams
        since 'output_filepath' is not valid keyword argument.
    """
    conf = {
        "filename": STATIC_DIR / filepath,
        "show": False,
        "direction": "LR" if horizontal else "TB",
        "outformat": "png",
        "graph_attr": {
            "bgcolor": "transparent",
        },
    }

    # If format name is defined, use it to guess output filename
    if conf.get("outformat"):
        conf["output_filepath"] = conf["filename"].with_suffix("." + conf["outformat"])
    # Else just adopt the original filename (wsithout any extension)
    else:
        conf["output_filepath"] = conf["filename"]

    if extra:
        conf.update(extra)

    return conf


def adjust_image(filepath, padding=10):
    """
    Adjust image to add padding and enforce white background.

    This will overwrite the given source image.

    Current code is only compatible with RGBA image and so with a PNG format.

    Arguments:
        filepath (pathlib.Path): Source path object.

    Keyword Arguments:
        padding (integer): Padding size in pixel, applied as both horizontal and
            vertical.

    Returns:
        PIL.Image: Final result image object.
    """
    source = Image.open(filepath)

    # Use getbbox to get the non empty content size so we get ride of the empty margins
    cropped = source.crop(source.getbbox())

    # Compute source cropped size to include padding
    width, height = cropped.size
    new_size = (
        width + (padding * 2),
        height + (padding * 2),
    )

    # Build new image from the cropped one plus additional padding
    padded = Image.new(
        cropped.mode,
        new_size,
        color=(255, 255, 255)
    )
    padded.paste(cropped, (padding, padding))

    # Build white background image
    white_background = Image.new(
        "RGBA",
        padded.size,
        color=(255, 255, 255)
    )
    # Merge
    alpha_composite = Image.alpha_composite(white_background, padded)
    alpha_composite.save(filepath)

    return alpha_composite
