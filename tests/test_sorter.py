import logging
import os
import unittest

from PIL import Image
from pexpect import expect

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_pixels
from pixel_sorting.sorters.basic import PixelSorter, Inverter, BasicSorter
from pixel_sorting.sorters.checker_board import CheckerBoardSorter, ExtendedCheckerBoardSorter
from pixel_sorting.sorters.circle import CircleSorter
from pixel_sorting.sorters.column import ColumnSorter, AlternatingColumnSorter
from pixel_sorting.sorters.diamond import DiamondSorter
from pixel_sorting.sorters.row import RowSorter, AlternatingRowSorter
from tests.test_helper import create_test_image, execute_sorter, execute_draw_pixel, execute_draw_octants, \
    execute_draw_circle

logging.getLogger().setLevel(logging.ERROR)
sorters_png = "./sorters.png"


class SorterTests(unittest.TestCase):
    def setUp(self):
        create_test_image(sorters_png, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        self.stencil_img = Image.open(sorters_png)

    def tearDown(self):
        os.remove(sorters_png)

    def testPixelSorter(self):
        sorter = PixelSorter("")
        sorter_pixels = []
        actual = sorter.sort_pixels(sorter_pixels, 0, 0, sort_criteria.built_in())
        expected = None
        self.assertEqual(expected, actual)

    def testInverter(self):
        inverter_pixels = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]

        inverter = Inverter()
        expected = [(255, 255, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 0)]
        actual = inverter.sort_pixels(inverter_pixels, 0, 0, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testBasicSorterBuiltIn(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testBasicSorterRed(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.red())
        self.assertEqual(expected, actual)

    def testBasicSorterGreen(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (23, 10, 15), (15, 11, 2), (12, 17, 5), (7, 24, 3), (16, 27, 18)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.green())
        self.assertEqual(expected, actual)

    def testBasicSorterBlue(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.blue())
        self.assertEqual(expected, actual)

    def testBasicSorterBrightness(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (23, 10, 15), (7, 24, 3), (16, 27, 18)]
        actual = basic_sorter.sort_pixels(basic_pixels, 0, 0, sort_criteria.brightness())
        self.assertEqual(expected, actual)

    def testBasicSorterAverage(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        expected = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]
        basic_sorter = BasicSorter()
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.avg())
        self.assertEqual(expected, actual)

    def testBasicSorterHue(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (7, 24, 3), (16, 27, 18), (23, 10, 15)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.hue())
        self.assertEqual(expected, actual)

    def testBasicSorterSaturation(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        exptected = [(16, 27, 18), (23, 10, 15), (12, 17, 5), (6, 3, 1), (15, 11, 2), (7, 24, 3)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.saturation())
        self.assertEqual(exptected, actual)

    def testBasicSorterLightness(self):
        basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
        basic_sorter = BasicSorter()
        expected = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (7, 24, 3), (23, 10, 15), (16, 27, 18)]
        actual = basic_sorter.sort_pixels(basic_pixels.copy(), 0, 0, sort_criteria.lightness())
        self.assertEqual(expected, actual)

    def testRowSorter(self):
        row_pixels = [4, 2, 3, 5, 1,
                      3, 1, 5, 2, 4]

        row_sorter = RowSorter(0)
        expected = [1, 2, 3, 4, 5,
                    3, 1, 5, 2, 4]
        actual = row_sorter.sort_pixels(row_pixels.copy(), 5, 2, sort_criteria.built_in())
        self.assertEqual(actual, expected)

        row_sorter = RowSorter(1, True)
        expected = [4, 2, 3, 5, 1,
                    5, 4, 3, 2, 1]
        actual = row_sorter.sort_pixels(row_pixels.copy(), 5, 2, sort_criteria.built_in())
        self.assertEqual(actual, expected)

    def testAlternatingRowSorter(self):
        alt_pixels = [p for p in range(1, 26)]

        row_sorter = AlternatingRowSorter(alternation=1)
        expected = [1, 2, 3, 4, 5, 10, 9, 8, 7, 6, 11, 12, 13, 14, 15, 20, 19, 18, 17, 16, 21, 22, 23, 24, 25]
        actual = row_sorter.sort_pixels(alt_pixels.copy(), 5, 5, sort_criteria.built_in())
        self.assertEqual(actual, expected)

    def testColumnSorter(self):
        col_pixels = [4, 7, 3, 9, 1, 6, 5, 8, 2, 10]

        col_sorter = ColumnSorter(0, False)
        expected = [1, 7, 2, 9, 3, 6, 4, 8, 5, 10]
        actual = col_sorter.sort_pixels(col_pixels.copy(), 2, 5, sort_criteria.built_in())
        self.assertEqual(actual, expected)

        col_sorter = ColumnSorter(1, True)
        expected = [4, 10, 3, 9, 1, 8, 5, 7, 2, 6]
        actual = col_sorter.sort_pixels(col_pixels.copy(), 2, 5, sort_criteria.built_in())
        self.assertEqual(actual, expected)

    def testAlternatingColumnSorter(self):
        alt_pixels = [p for p in range(1, 26)]

        col_sorter = AlternatingColumnSorter(1)
        expected = [1, 22, 3, 24, 5, 6, 17, 8, 19, 10, 11, 12, 13, 14, 15, 16, 7, 18, 9, 20, 21, 2, 23, 4, 25]
        actual = col_sorter.sort_pixels(alt_pixels.copy(), 5, 5, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testDiamondSorterNextPosition(self):
        self.assertEqual(DiamondSorter.next_position((0, 0)), (1, 0))
        self.assertEqual(DiamondSorter.next_position((1, 0)), (0, 1))
        self.assertEqual(DiamondSorter.next_position((0, 1)), (-1, 0))
        self.assertEqual(DiamondSorter.next_position((-1, 0)), (0, -1))
        self.assertEqual(DiamondSorter.next_position((0, -1)), (2, 0))

        self.assertEqual(DiamondSorter.next_position((2, 0)), (1, 1))
        self.assertEqual(DiamondSorter.next_position((1, 1)), (0, 2))
        self.assertEqual(DiamondSorter.next_position((0, 2)), (-1, 1))
        self.assertEqual(DiamondSorter.next_position((-1, 1)), (-2, 0))
        self.assertEqual(DiamondSorter.next_position((-2, 0)), (-1, -1))
        self.assertEqual(DiamondSorter.next_position((-1, -1)), (0, -2))
        self.assertEqual(DiamondSorter.next_position((0, -2)), (1, -1))
        self.assertEqual(DiamondSorter.next_position((1, -1)), (3, 0))

        self.assertEqual(DiamondSorter.next_position((3, 0)), (2, 1))
        self.assertEqual(DiamondSorter.next_position((2, 1)), (1, 2))
        self.assertEqual(DiamondSorter.next_position((1, 2)), (0, 3))
        self.assertEqual(DiamondSorter.next_position((0, 3)), (-1, 2))
        self.assertEqual(DiamondSorter.next_position((-1, 2)), (-2, 1))
        self.assertEqual(DiamondSorter.next_position((-2, 1)), (-3, 0))
        self.assertEqual(DiamondSorter.next_position((-3, 0)), (-2, -1))
        self.assertEqual(DiamondSorter.next_position((-2, -1)), (-1, -2))
        self.assertEqual(DiamondSorter.next_position((-1, -2)), (0, -3))
        self.assertEqual(DiamondSorter.next_position((0, -3)), (1, -2))
        self.assertEqual(DiamondSorter.next_position((1, -2)), (2, -1))
        self.assertEqual(DiamondSorter.next_position((2, -1)), (4, 0))

        self.assertEqual(DiamondSorter.next_position((4, 0)), (3, 1))
        self.assertEqual(DiamondSorter.next_position((3, 1)), (2, 2))
        self.assertEqual(DiamondSorter.next_position((2, 2)), (1, 3))
        self.assertEqual(DiamondSorter.next_position((1, 3)), (0, 4))
        self.assertEqual(DiamondSorter.next_position((0, 4)), (-1, 3))
        self.assertEqual(DiamondSorter.next_position((-1, 3)), (-2, 2))
        self.assertEqual(DiamondSorter.next_position((-2, 2)), (-3, 1))
        self.assertEqual(DiamondSorter.next_position((-3, 1)), (-4, 0))
        self.assertEqual(DiamondSorter.next_position((-4, 0)), (-3, -1))
        self.assertEqual(DiamondSorter.next_position((-3, -1)), (-2, -2))
        self.assertEqual(DiamondSorter.next_position((-2, -2)), (-1, -3))
        self.assertEqual(DiamondSorter.next_position((-1, -3)), (0, -4))
        self.assertEqual(DiamondSorter.next_position((0, -4)), (1, -3))
        self.assertEqual(DiamondSorter.next_position((1, -3)), (2, -2))
        self.assertEqual(DiamondSorter.next_position((2, -2)), (3, -1))
        self.assertEqual(DiamondSorter.next_position((3, -1)), (5, 0))

    def testDiamondSorter(self):
        diamond_pixels = [p for p in range(1, 26)]
        diamond_sorter = DiamondSorter()
        expected = [24, 19, 12, 20, 25,
                    18, 11, 5, 13, 21,
                    10, 4, 1, 2, 6,
                    17, 9, 3, 7, 14,
                    23, 16, 8, 15, 22]
        actual = diamond_sorter.sort_pixels(diamond_pixels, 5, 5, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testCheckerBoardSorter1(self):
        board_square = [p for p in range(1, 16 * 16 + 1)[::-1]]
        board_sorter = CheckerBoardSorter()
        expected = [239, 240, 237, 238, 235, 236, 233, 234, 231, 232, 229, 230, 227, 228, 225, 226, 255, 256, 253, 254,
                    251, 252, 249, 250, 247, 248, 245, 246, 243, 244, 241, 242, 207, 208, 205, 206, 203, 204, 201, 202,
                    199, 200, 197, 198, 195, 196, 193, 194, 223, 224, 221, 222, 219, 220, 217, 218, 215, 216, 213, 214,
                    211, 212, 209, 210, 175, 176, 173, 174, 171, 172, 169, 170, 167, 168, 165, 166, 163, 164, 161, 162,
                    191, 192, 189, 190, 187, 188, 185, 186, 183, 184, 181, 182, 179, 180, 177, 178, 143, 144, 141, 142,
                    139, 140, 137, 138, 135, 136, 133, 134, 131, 132, 129, 130, 159, 160, 157, 158, 155, 156, 153, 154,
                    151, 152, 149, 150, 147, 148, 145, 146, 111, 112, 109, 110, 107, 108, 105, 106, 103, 104, 101, 102,
                    99, 100, 97, 98, 127, 128, 125, 126, 123, 124, 121, 122, 119, 120, 117, 118, 115, 116, 113, 114, 79,
                    80, 77, 78, 75, 76, 73, 74, 71, 72, 69, 70, 67, 68, 65, 66, 95, 96, 93, 94, 91, 92, 89, 90, 87, 88,
                    85, 86, 83, 84, 81, 82, 47, 48, 45, 46, 43, 44, 41, 42, 39, 40, 37, 38, 35, 36, 33, 34, 63, 64, 61,
                    62, 59, 60, 57, 58, 55, 56, 53, 54, 51, 52, 49, 50, 15, 16, 13, 14, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4,
                    1, 2, 31, 32, 29, 30, 27, 28, 25, 26, 23, 24, 21, 22, 19, 20, 17, 18]

        actual = board_sorter.sort_pixels(board_square.copy(), 16, 16, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testCheckerBoardSorter2(self):
        board_square = [p for p in range(1, 16 * 16 + 1)[::-1]]
        board_sorter = CheckerBoardSorter(sorter=CircleSorter())
        expected = [239, 240, 237, 238, 235, 236, 233, 234, 231, 232, 229, 230, 227, 228, 225, 226, 255, 256, 253, 254,
                    251, 252, 249, 250, 247, 248, 245, 246, 243, 244, 241, 242, 207, 208, 205, 206, 203, 204, 201, 202,
                    199, 200, 197, 198, 195, 196, 193, 194, 223, 224, 221, 222, 219, 220, 217, 218, 215, 216, 213, 214,
                    211, 212, 209, 210, 175, 176, 173, 174, 171, 172, 169, 170, 167, 168, 165, 166, 163, 164, 161, 162,
                    191, 192, 189, 190, 187, 188, 185, 186, 183, 184, 181, 182, 179, 180, 177, 178, 143, 144, 141, 142,
                    139, 140, 137, 138, 135, 136, 133, 134, 131, 132, 129, 130, 159, 160, 157, 158, 155, 156, 153, 154,
                    151, 152, 149, 150, 147, 148, 145, 146, 111, 112, 109, 110, 107, 108, 105, 106, 103, 104, 101, 102,
                    99, 100, 97, 98, 127, 128, 125, 126, 123, 124, 121, 122, 119, 120, 117, 118, 115, 116, 113, 114, 79,
                    80, 77, 78, 75, 76, 73, 74, 71, 72, 69, 70, 67, 68, 65, 66, 95, 96, 93, 94, 91, 92, 89, 90, 87, 88,
                    85, 86, 83, 84, 81, 82, 47, 48, 45, 46, 43, 44, 41, 42, 39, 40, 37, 38, 35, 36, 33, 34, 63, 64, 61,
                    62, 59, 60, 57, 58, 55, 56, 53, 54, 51, 52, 49, 50, 15, 16, 13, 14, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4,
                    1, 2, 31, 32, 29, 30, 27, 28, 25, 26, 23, 24, 21, 22, 19, 20, 17, 18]

        actual = board_sorter.sort_pixels(board_square.copy(), 16, 16, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testExtendedCheckerBoardSorter1(self):
        board_square = [p for p in range(1, 16 * 16 + 1)[::-1]]
        board_sorter = ExtendedCheckerBoardSorter()
        expected = [239, 240, 237, 238, 235, 236, 233, 234, 231, 232, 229, 230, 227, 228, 225, 226, 255, 256, 253, 254,
                    251, 252, 249, 250, 247, 248, 245, 246, 243, 244, 241, 242, 207, 208, 205, 206, 203, 204, 201, 202,
                    199, 200, 197, 198, 195, 196, 193, 194, 223, 224, 221, 222, 219, 220, 217, 218, 215, 216, 213, 214,
                    211, 212, 209, 210, 175, 176, 173, 174, 171, 172, 169, 170, 167, 168, 165, 166, 163, 164, 161, 162,
                    191, 192, 189, 190, 187, 188, 185, 186, 183, 184, 181, 182, 179, 180, 177, 178, 143, 144, 141, 142,
                    139, 140, 137, 138, 135, 136, 133, 134, 131, 132, 129, 130, 159, 160, 157, 158, 155, 156, 153, 154,
                    151, 152, 149, 150, 147, 148, 145, 146, 111, 112, 109, 110, 107, 108, 105, 106, 103, 104, 101, 102,
                    99, 100, 97, 98, 127, 128, 125, 126, 123, 124, 121, 122, 119, 120, 117, 118, 115, 116, 113, 114, 79,
                    80, 77, 78, 75, 76, 73, 74, 71, 72, 69, 70, 67, 68, 65, 66, 95, 96, 93, 94, 91, 92, 89, 90, 87, 88,
                    85, 86, 83, 84, 81, 82, 47, 48, 45, 46, 43, 44, 41, 42, 39, 40, 37, 38, 35, 36, 33, 34, 63, 64, 61,
                    62, 59, 60, 57, 58, 55, 56, 53, 54, 51, 52, 49, 50, 15, 16, 13, 14, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4,
                    1, 2, 31, 32, 29, 30, 27, 28, 25, 26, 23, 24, 21, 22, 19, 20, 17, 18]
        actual = board_sorter.sort_pixels(board_square, 16, 16, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testExtendedCheckerBoardSorter2(self):
        board_square = [p for p in range(1, 16 * 16 + 1)[::-1]]
        criterias = [sort_criteria.built_in()]
        sorters = [BasicSorter]
        board_sorter = ExtendedCheckerBoardSorter(width=2, height=2, criterias=criterias, sorters=sorters)
        expected = [137, 138, 139, 140, 141, 142, 143, 144, 129, 130, 131, 132, 133, 134, 135, 136, 153,
                    154, 155, 156, 157, 158, 159, 160, 145, 146, 147, 148, 149, 150, 151, 152, 169, 170,
                    171, 172, 173, 174, 175, 176, 161, 162, 163, 164, 165, 166, 167, 168, 185, 186, 187,
                    188, 189, 190, 191, 192, 177, 178, 179, 180, 181, 182, 183, 184, 201, 202, 203, 204,
                    205, 206, 207, 208, 193, 194, 195, 196, 197, 198, 199, 200, 217, 218, 219, 220, 221,
                    222, 223, 224, 209, 210, 211, 212, 213, 214, 215, 216, 233, 234, 235, 236, 237, 238,
                    239, 240, 225, 226, 227, 228, 229, 230, 231, 232, 249, 250, 251, 252, 253, 254, 255,
                    256, 241, 242, 243, 244, 245, 246, 247, 248, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4,
                    5, 6, 7, 8, 25, 26, 27, 28, 29, 30, 31, 32, 17, 18, 19, 20, 21, 22, 23, 24, 41, 42, 43,
                    44, 45, 46, 47, 48, 33, 34, 35, 36, 37, 38, 39, 40, 57, 58, 59, 60, 61, 62, 63, 64, 49,
                    50, 51, 52, 53, 54, 55, 56, 73, 74, 75, 76, 77, 78, 79, 80, 65, 66, 67, 68, 69, 70, 71,
                    72, 89, 90, 91, 92, 93, 94, 95, 96, 81, 82, 83, 84, 85, 86, 87, 88, 105, 106, 107, 108,
                    109, 110, 111, 112, 97, 98, 99, 100, 101, 102, 103, 104, 121, 122, 123, 124, 125, 126,
                    127, 128, 113, 114, 115, 116, 117, 118, 119, 120]
        actual = board_sorter.sort_pixels(board_square, 16, 16, None)
        self.assertEqual(expected, actual)


class CircleSorterTest(unittest.TestCase):
    def setUp(self):
        create_test_image(sorters_png, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        self.stencil_img = Image.open(sorters_png)

    def tearDown(self):
        os.remove(sorters_png)

    @staticmethod
    def circle_sorter_draw_pixel_setup():
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        expected = [1, 2, 3, 4, 5,
                    6, 7, 8, 9, 10,
                    11, 12, 13, 50, 15,
                    16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25]
        circle_sorter = CircleSorter()
        return circle_pixels, circle_sorter, expected, pixel_source

    def testPixel1(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()
        expected_pixel = 1
        index, img_width, img_height, x, y = 0, 5, 5, 1, 0
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(circle_pixels, expected)

    @unittest.skip("Investigate why this is failing")
    def testPixel2(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()
        expected_pixel = 0
        index, img_width, img_height, x, y = 0, 5, 5, 3, 0
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(expected, circle_pixels)

    @unittest.skip("Investigate why this is failing")
    def testPixel3(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()

        # execute_draw_pixel(self, circle_sorter, -3, 0, 0, circle_pixels, 0, circle_pixels, pixel_source)
        expected_pixel = 0
        index, img_width, img_height, x, y = 0, 5, 5, -3, 0
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(circle_pixels, expected)

    @unittest.skip("Investigate why this is failing")
    def testPixel4(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()

        # execute_draw_pixel(self, circle_sorter, 0, -3, 0, circle_pixels, 0, circle_pixels, pixel_source)
        expected_pixel = 0
        index, img_width, img_height, x, y = 0, 5, 5, 0, -3
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(circle_pixels, expected)

    @unittest.skip("Investigate why this is failing")
    def testPixel5(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()

        # execute_draw_pixel(self, circle_sorter, -3, -3, 0, circle_pixels, 0, circle_pixels, pixel_source)
        expected_pixel = 0
        index, img_width, img_height, x, y = 0, 5, 5, -3, -3
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(circle_pixels, expected)

    @unittest.skip("Investigate why this is failing")
    def testPixel6(self):
        circle_pixels, circle_sorter, expected, pixel_source = self.circle_sorter_draw_pixel_setup()
        expected_pixel = 0
        index, img_width, img_height, x, y = len(pixel_source), 5, 5, 1, 0
        actual = circle_sorter.draw_pixel(circle_pixels, pixel_source.copy(), index, img_width, img_height, x, y)
        self.assertEqual(expected_pixel, actual)
        self.assertEqual(circle_pixels, expected)

    def testOctant1(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]

        circle_sorter = CircleSorter()
        expected = [1, 2, 3, 4, 5,
                    6, 7, 53, 9, 10,
                    11, 51, 13, 50, 15,
                    16, 17, 52, 19, 20,
                    21, 22, 23, 24, 25]
        index, img_width, img_height, x, y = 0, 5, 5, 1, 0
        actual_index = circle_sorter.draw_octant_pixels(circle_pixels, pixel_source, index, img_width, img_height, x, y)
        expected_index = 4
        self.assertEqual(expected_index, actual_index)
        self.assertEqual(circle_pixels, expected)

    def testOctant2(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]

        circle_sorter = CircleSorter()
        expected = [1, 2, 3, 4, 5,
                    6, 52, 8, 53, 10,
                    11, 12, 13, 14, 15,
                    16, 51, 18, 50, 20,
                    21, 22, 23, 24, 25]
        index, img_width, img_height, x, y = 0, 5, 5, 1, 1
        actual_index = circle_sorter.draw_octant_pixels(circle_pixels, pixel_source.copy(), index, img_width,
                                                        img_height, x, y)
        expected_index = 4
        self.assertEqual(expected_index, actual_index)
        self.assertEqual(circle_pixels, expected)

    def testOctant3(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        expected = [1, 57, 3, 55, 5,
                    52, 7, 8, 9, 53,
                    11, 12, 13, 14, 15,
                    51, 17, 18, 19, 50,
                    21, 56, 23, 54, 25]
        index, img_width, img_height, x, y = 0, 5, 5, 2, 1
        actual_index = circle_sorter.draw_octant_pixels(circle_pixels, pixel_source.copy(), index, img_width,
                                                        img_height, x, y)
        expected_index = 8
        self.assertEqual(expected_index, actual_index)
        self.assertEqual(circle_pixels, expected)

    def testDrawCircle1(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        circle_radius_result1 = [1, 2, 3, 4, 5,
                                 6, 7, 53, 9, 10,
                                 11, 51, 13, 50, 15,
                                 16, 17, 52, 19, 20,
                                 21, 22, 23, 24, 25]
        execute_draw_circle(self, circle_sorter, circle_radius_result1, 1, circle_pixels, pixel_source)

    def testDrawCircle2(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        circle_radius_result2 = [1, 2, 3, 4, 5,
                                 6, 56, 53, 57, 10,
                                 11, 51, 13, 50, 15,
                                 16, 55, 52, 54, 20,
                                 21, 22, 23, 24, 25]
        execute_draw_circle(self, circle_sorter, circle_radius_result2, 1.5, circle_pixels, pixel_source)

    def testDrawCircle3(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        circle_radius_result3 = [1, 61, 53, 59, 5,
                                 56, 7, 8, 9, 57,
                                 51, 12, 13, 14, 50,
                                 55, 17, 18, 19, 54,
                                 21, 60, 52, 58, 25]
        execute_draw_circle(self, circle_sorter, circle_radius_result3, 2, circle_pixels, pixel_source)

    def testDrawCircle4(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        circle_radius_result4 = [1, 61, 53, 59, 5,
                                 56, 7, 8, 9, 57,
                                 51, 12, 13, 14, 50,
                                 55, 17, 18, 19, 54,
                                 21, 60, 52, 58, 25]
        execute_draw_circle(self, circle_sorter, circle_radius_result4, 2.5, circle_pixels, pixel_source)

    def testDrawCircle5(self):
        pixel_source = [p for p in range(50, 99)]
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        circle_radius_result5 = [52, 2, 3, 4, 53,
                                 6, 7, 8, 9, 10,
                                 11, 12, 13, 14, 15,
                                 16, 17, 18, 19, 20,
                                 51, 22, 23, 24, 50]
        execute_draw_circle(self, circle_sorter, circle_radius_result5, 3, circle_pixels, pixel_source)

    @unittest.skip("Center pixel is not being sorted correctly")
    def testSorter(self):
        circle_pixels = [p for p in range(1, 26)]
        circle_sorter = CircleSorter()
        expected = [24, 21, 13, 19, 25,
                    16, 8, 5, 9, 17,
                    11, 3, 1, 2, 10,
                    15, 7, 4, 6, 14,
                    23, 20, 12, 18, 22]
        actual = circle_sorter.sort_pixels(circle_pixels.copy(), 5, 5, sort_criteria.built_in())
        self.assertEqual(expected, actual)

    def testWithRealFile(self):
        img = Image.open(sorters_png)
        img_width = img.size[0]
        img_height = img.size[1]

        pixels = get_pixels(img)

        pixel_dict = {}
        for p in pixels:
            if p not in pixel_dict:
                pixel_dict[p] = 0
            pixel_dict[p] += 1

        new_pixels = [p for p in pixels]

        circle_sorter = CircleSorter()
        circle_sorter.sort_pixels(new_pixels, img_width, img_height, sort_criteria.built_in())

        self.assertEqual(len(new_pixels), len(pixels), "The new image doesn't have the same number of pixels.")
        for p in new_pixels:
            self.assertTrue(p in pixels)

        new_pixel_dict = {}
        for p in pixels:
            if p not in new_pixel_dict:
                new_pixel_dict[p] = 0
            new_pixel_dict[p] += 1

        for p in new_pixel_dict:
            self.assertTrue(p in pixel_dict)
            self.assertEqual(new_pixel_dict[p], pixel_dict[p])
