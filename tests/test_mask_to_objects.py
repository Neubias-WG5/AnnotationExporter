from unittest import TestCase, skip

import numpy as np
from PIL.Image import fromarray
from PIL.ImageDraw import ImageDraw
from cv2 import imwrite

from annotation_exporter import mask_to_objects_2d
from shapely.geometry import Point, Polygon, box


def draw_square(image, side, center, color):
    """Draw a square centered in 'center' and of which the side has 'side'"""
    top_left = (center[1] - side / 2, center[0] - side / 2)
    top_right = (center[1] + side / 2, center[0] - side / 2)
    bottom_left = (center[1] - side / 2, center[0] + side / 2)
    bottom_right = (center[1] + side / 2, center[0] + side / 2)
    p = Polygon([top_left, top_right, bottom_right, bottom_left, top_left])
    return draw_poly(image, p, color)


def draw_square_by_corner(image, side, top_left, color):
    top_left = (top_left[1], top_left[0])
    top_right = (top_left[0] + side, top_left[1])
    bottom_left = (top_left[0], top_left[1] + side)
    bottom_right = (top_left[0] + side, top_left[1] + side)
    p = Polygon([top_left, top_right, bottom_right, bottom_left, top_left])
    return draw_poly(image, p, color)


def draw_circle(image, radius, center, color=255, return_circle=False):
    """Draw a circle of radius 'radius' and centered in 'centered'"""
    circle_center = Point(*center)
    circle_polygon = circle_center.buffer(radius)
    image_out = draw_poly(image, circle_polygon, color)
    if return_circle:
        return image_out, circle_polygon
    else:
        return image_out


def draw_poly(image, polygon, color=255):
    """Draw a polygon in the given color at the given location"""
    pil_image = fromarray(image)
    validated_color = color
    draw = ImageDraw(pil_image)
    if len(image.shape) > 2 and image.shape[2] > 1:
        validated_color = tuple(color)
    draw.polygon(polygon.boundary.coords, fill=validated_color, outline=validated_color)
    return np.asarray(pil_image)


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

        imwrite("test.png", image)
        slices = mask_to_objects_2d(image)
        # sort by bounding box top left corner
        slices = sorted(slices, key=lambda s: s.polygon.bounds[:2])

        self.assertEqual(len(slices), 2)
        self.assertEqual(slices[0].label, 255)
        self.assertEqual(slices[1].label, 127)
