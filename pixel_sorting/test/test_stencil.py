import unittest

from PIL import Image

from PixelFun import src


# from src.Stencils import *


class StencilTests(unittest.TestCase):

    stencil_pixels = []
    stencil_img = Image.open("test_image.png")
    stencil_input_pixels = []

    def testStencil(self):
        stencil = src.Stencil(4, 4, 2, 2)
        self.assertEqual(stencil.cut_out_pixels(self.stencil_pixels), None)
        self.assertEqual(stencil.cut_out_image(self.stencil_img), None)
        self.assertEqual(stencil.put_in_pixels(self.stencil_pixels, self.stencil_input_pixels), None)
        self.assertEqual(stencil.put_in_image(self.stencil_img, self.stencil_input_pixels), None)

    rect_pixels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    rect_out_result = [6, 7, 10, 11]
    rect_in_result = [6, 7, 3, 4, 10, 11, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    rect_edge_result = [16]

    def testRectangle(self):
        reference_pixels = [p for p in self.rect_pixels]

        rect = src.RectangleStencil(4, 4, 1, 1, 2, 2)
        self.assertEqual(rect.cut_out_pixels(self.rect_pixels), self.rect_out_result)
        self.assertEqual(self.rect_pixels, reference_pixels)

        rect.x = 0
        rect.y = 0
        test_pixels = [p for p in self.rect_pixels]
        self.assertEqual(rect.put_in_pixels(test_pixels, self.rect_out_result), self.rect_in_result)
        self.assertEqual(test_pixels, self.rect_in_result)

        rect.x = 3
        rect.y = 3
        self.assertEqual(rect.cut_out_pixels(self.rect_pixels), self.rect_edge_result)
        self.assertEqual(self.rect_pixels, reference_pixels)

        rect.x = 4
        self.assertRaises(Exception, rect.cut_out_pixels, self.rect_pixels)

        rect.x = 2
        rect.y = 4
        self.assertRaises(Exception, rect.cut_out_pixels, self.rect_pixels)

    circ_pixels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    circ_out_result1 = [8, 12, 13, 14, 18]
    circ_out_result2 = [3, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 23]
    circ_out_result3 = [2, 6, 7, 8, 12]
    circ_in = [13, 17, 18, 19, 111, 112, 113, 114, 115, 117, 118, 119, 123]
    circ_in_result1 = [1, 2, 13, 4, 5, 6, 17, 18, 19, 10, 111, 112, 113, 114, 115, 16, 117, 118, 119, 20, 21, 22, 123, 24, 25]
    circ_in_result2 = [1, 8, 3, 4, 5, 12, 13, 14, 9, 10, 11, 18, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    def testCirlce(self):
        reference_pixels = [p for p in self.circ_pixels]
        circle = src.CircleStencil(5, 5, 2, 2, 1)
        self.assertEqual(circle.cut_out_pixels(self.circ_pixels), self.circ_out_result1)
        self.assertEqual(self.circ_pixels, reference_pixels)

        circle.radius = 2
        self.assertEqual(circle.cut_out_pixels(self.circ_pixels), self.circ_out_result2)
        self.assertEqual(self.circ_pixels, reference_pixels)

        test_pixels = [p for p in self.circ_pixels]
        self.assertEqual(circle.put_in_pixels(test_pixels, self.circ_in), self.circ_in_result1)
        self.assertEqual(test_pixels, self.circ_in_result1)

        circle.radius = 1
        circle.x = 1
        circle.y = 1
        self.assertEqual(circle.cut_out_pixels(self.circ_pixels), self.circ_out_result3)

        self.assertEqual(circle.put_in_pixels(self.circ_pixels, self.circ_out_result1), self.circ_in_result2)
