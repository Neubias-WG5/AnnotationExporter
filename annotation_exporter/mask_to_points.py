import numpy as np
from shapely.geometry import Point, box

from annotation_exporter import AnnotationSlice


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