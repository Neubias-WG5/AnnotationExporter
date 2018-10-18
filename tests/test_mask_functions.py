from unittest import TestCase

import numpy as np

from annotation_exporter import mask_to_objects_2d
from shapely.geometry import Polygon, box

from tests.util import draw_square_by_corner, draw_poly


class TestMaskToObject2D(TestCase):
    def testExportOneSquare(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 100, (150, 50), color=255)

        slices = mask_to_objects_2d(image)

        self.assertEqual(len(slices), 1)
        self.assertEqual(slices[0].label, 255)
        self.assertTrue(slices[0].polygon.equals(box(50, 150, 150, 250)), msg="Polygon is equal")

    def testOffset(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 100, (150, 50), color=255)

        slices = mask_to_objects_2d(image, offset=(255, 320))

        self.assertEqual(len(slices), 1)
        self.assertEqual(slices[0].label, 255)
        self.assertTrue(slices[0].polygon.equals(box(305, 470, 405, 570)), msg="Polygon is equal")

    def testSeveralObjects(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 50, (150, 50), color=255)
        image = draw_square_by_corner(image, 50, (205, 105), color=127)

        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertTrue(slices[0].polygon.equals(box(50, 150, 100, 200)), msg="Polygon is equal")
        self.assertEqual(slices[1].label, 127)
        self.assertTrue(slices[1].polygon.equals(box(105, 205, 155, 255)), msg="Polygon is equal")

    def testMultipartPolygon(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 50, (150, 50), color=255)
        image = draw_square_by_corner(image, 50, (201, 101), color=127)

        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertEqual(slices[1].label, 127)

    def testAdjacentWithoutSeperation(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 50, (150, 50), color=255)
        image = draw_square_by_corner(image, 50, (150, 101), color=127)

        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertEqual(slices[1].label, 127)

    def testAdjacentWithSeparation(self):
        image = np.zeros([300, 200], dtype=np.int)
        image = draw_square_by_corner(image, 50, (150, 50), color=255)
        image = draw_square_by_corner(image, 50, (150, 102), color=127)

        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertTrue(slices[0].polygon.equals(box(50, 150, 100, 200)), msg="Polygon is equal")
        self.assertEqual(slices[1].label, 127)
        self.assertTrue(slices[1].polygon.equals(box(102, 150, 152, 200)), msg="Polygon is equal")

    def testSmallObject(self):
        image = np.zeros([100, 100], dtype=np.int)
        image = draw_poly(image, Polygon([(15, 77), (15, 78), (16, 78), (15, 77)]), color=127)
        image = draw_poly(image, box(1, 1, 2, 2), color=255)

        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertEqual(slices[1].label, 127)