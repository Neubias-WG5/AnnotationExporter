from unittest import TestCase
import numpy as np
from shapely.geometry import Point, Polygon, box

from annotation_exporter import mask_to_points_2d


class TestMaskToPoints(TestCase):
    def testSinglePoint(self):
        image = np.zeros([50, 50], dtype=np.int)
        image[5, 6] = 125

        slices = mask_to_points_2d(image)

        self.assertEqual(len(slices), 1)
        self.assertIsInstance(slices[0].polygon, Point)
        self.assertEqual(slices[0].polygon.x, 6)
        self.assertEqual(slices[0].polygon.y, 5)

    def testSinglePointEncodedSquare(self):
        image = np.zeros([50, 50], dtype=np.int)
        image[5, 6] = 125

        slices = mask_to_points_2d(image, points=False)

        self.assertEqual(len(slices), 1)
        self.assertIsInstance(slices[0].polygon, Polygon)
        self.assertTrue(slices[0].polygon.equals(box(5, 4, 7, 6)))