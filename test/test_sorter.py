import unittest

from PixelSorters import *


class SorterTests(unittest.TestCase):

    sorter_img = Image.open("test_image.png")
    sorter_pixels = []

    def testPixelSorter(self):
        sorter = PixelSorter()
        self.assertEqual(sorter.sort_image(self.sorter_img), None)
        self.assertEqual(sorter.sort_pixels(self.sorter_pixels), None)

    inverter_pixels = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    inverter_result = [(255, 255, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 0)]

    def testInverter(self):
        inverter = Inverter()
        test_pixels = [p for p in self.inverter_pixels]
        self.assertEqual(inverter.sort_pixels(test_pixels), self.inverter_result)
        self.assertEqual(test_pixels, self.inverter_result)

    basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
    basic_builtin_result = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
    basic_red_result = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
    basic_green_result = [(6, 3, 1), (23, 10, 15), (15, 11, 2), (12, 17, 5), (7, 24, 3), (16, 27, 18)]
    basic_blue_result = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]
    basic_brightness_result = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (23, 10, 15), (7, 24, 3), (16, 27, 18)]
    basic_avg_result = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]

    def testBasicSorter(self):
        basic_sorter = BasicSorter(BuiltInSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_builtin_result)
        self.assertEqual(test_pixels, self.basic_builtin_result)

        basic_sorter = BasicSorter(RedSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_red_result)
        self.assertEqual(test_pixels, self.basic_red_result)

        basic_sorter = BasicSorter(GreenSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_green_result)
        self.assertEqual(test_pixels, self.basic_green_result)

        basic_sorter = BasicSorter(BlueSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_blue_result)
        self.assertEqual(test_pixels, self.basic_blue_result)

        basic_sorter = BasicSorter(BrightnessSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_brightness_result)
        self.assertEqual(test_pixels, self.basic_brightness_result)

        basic_sorter = BasicSorter(AvgSort)
        test_pixels = [p for p in self.basic_pixels]
        self.assertEqual(basic_sorter.sort_pixels(test_pixels), self.basic_avg_result)
        self.assertEqual(test_pixels, self.basic_avg_result)

    row_pixels = [4, 2, 3, 5, 1,
                  3, 1, 5, 2, 4]
    row_result1 = [1, 2, 3, 4, 5,
                   3, 1, 5, 2, 4]
    row_result2 = [4, 2, 3, 5, 1,
                   5, 4, 3, 2, 1]

    def testRowSorter(self):
        row_sorter = RowSorter(5, 2, BuiltInSort, 0)
        test_pixels = [p for p in self.row_pixels]
        self.assertEqual(row_sorter.sort_pixels(test_pixels), self.row_result1)
        self.assertEqual(test_pixels, self.row_result1)

        row_sorter = RowSorter(5, 2, BuiltInSort, 1, True)
        test_pixels = [p for p in self.row_pixels]
        self.assertEqual(row_sorter.sort_pixels(test_pixels), self.row_result2)
        self.assertEqual(test_pixels, self.row_result2)

    alt_pixels = [p for p in range(1, 26)]
    alt_row_result = [1, 2, 3, 4, 5, 10, 9, 8, 7, 6, 11, 12, 13, 14, 15, 20, 19, 18, 17, 16, 21, 22, 23, 24, 25]

    def testAlternatingRowSorter(self):
        row_sorter = AlternatingRowSorter(5, 5, BuiltInSort, 1)
        test_pixels = [p for p in self.alt_pixels]
        self.assertEqual(row_sorter.sort_pixels(test_pixels), self.alt_row_result)
        self.assertEqual(test_pixels, self.alt_row_result)

    col_pixels = [4, 7, 3, 9, 1, 6, 5, 8, 2, 10]
    col_result1 = [1, 7, 2, 9, 3, 6, 4, 8, 5, 10]
    col_result2 = [4, 10, 3, 9, 1, 8, 5, 7, 2, 6]

    def testColumnSorter(self):
        col_sorter = ColumnSorter(2, 5, BuiltInSort, 0, False)
        test_pixels = [p for p in self.col_pixels]
        self.assertEqual(col_sorter.sort_pixels(test_pixels), self.col_result1)
        self.assertEqual(test_pixels, self.col_result1)

        col_sorter.column = 1
        col_sorter.reverse = True
        test_pixels = [p for p in self.col_pixels]
        self.assertEqual(col_sorter.sort_pixels(test_pixels), self.col_result2)
        self.assertEqual(test_pixels, self.col_result2)

    alt_col_result = [1, 22, 3, 24, 5, 6, 17, 8, 19, 10, 11, 12, 13, 14, 15, 16, 7, 18, 9, 20, 21, 2, 23, 4, 25]

    def testAlternatingColumnSorter(self):
        col_sorter = AlternatingColumnSorter(5, 5, BuiltInSort, 1)
        test_pixels = [p for p in self.alt_pixels]
        self.assertEqual(col_sorter.sort_pixels(test_pixels), self.alt_col_result)
        self.assertEqual(test_pixels, self.alt_col_result)
