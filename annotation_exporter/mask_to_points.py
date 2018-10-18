import numpy as np
from shapely.geometry import Point, box

from annotation_exporter import AnnotationSlice
from annotation_exporter.export_util import draw_slice


def mask_to_points_2d(mask, points=True):
    """Converts a point label mask to a set of points.

    Parameters
    ----------
    mask: ndarray
        The point label mask
    points: bool
        Whether or not the object must be encoded as points (i.e. Point) of square polygons (i.e. 3 by 3 square Polygon)

    Returns
    -------
    slices: list
        List of annotations slices
    """
    pixels = np.nonzero(mask)
    labels = mask[pixels]
    return [
        AnnotationSlice(
            polygon=Point(x, y) if points else box(x - 1, y - 1, x + 1, y + 1),
            label=label
        ) for (y, x), label in zip(zip(*pixels), labels)
    ]


def csv_to_points(filepath, sep='\t', parse_fn=None, has_z=False, has_t=False, has_headers=False):
    """Extract a set of points coordinates from a csv file.
    Parameters
    ----------
    filepath: str
        Path of the csv file
    sep: str
        Separator used in the csv file
    parse_fn: callable
        A function to parse a csv line. It takes a full line as parameter (+ the separator) and should return the extracted coordinates
        in order: x, y, z, t. If z and/or t are present, it should be indicated by the has_z and/or has_t parameters.
    has_z: boolean
        True if there should be a z coordinate to read
    has_t: boolean
        True if there should be a t coordinate to read
    """
    points = list()
    with open(filepath, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if len(line) == 0 or (has_headers and i == 0):  # skip header or empty line
                continue
            if parse_fn is not None:  # should return the expected number of coordinates with valid type
                coords = parse_fn(line, sep)
            else:  # assumes "{x}sep{y}(sep{z})?(sep{t})?"
                splitted = line.split(sep)
                coords = [float(c) for c in splitted]

            # check number of dimensions
            expected_dim = 2
            if has_z:
                expected_dim += 1
            if has_t:
                expected_dim += 1

            if expected_dim != len(coords):
                raise ValueError("Invalid number of coordinates at line {} in file '{}'. Got {} dimensions while expecting {}.".format(i + 1, filepath, len(coords), expected_dim))

            # extract individual coordinates
            curr_index = 2
            x, y = coords[:curr_index]
            z, t = None, None
            if has_z:
                z = coords[curr_index]
                curr_index += 1
            if has_t:
                t = coords[curr_index]
                curr_index += 1

            points.append(AnnotationSlice(Point([x, y]), label=None, time=t, depth=z))
    return points


def slices_to_mask(slices, shape):
    """Transform annotation slices to a mask

    slices:
    shape:
    """
    mask = np.zeros(shape, np.int)
    for _slice in slices:
        mask = draw_slice(_slice, mask)
    return mask