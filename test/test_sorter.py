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
        self.assertEqual(inverter.sort_pixels(self.inverter_pixels), self.inverter_result)

    basic_pixels = [(1, 2, 3), (4, 5, 6), (10, 11, 12), (7, 8, 9), (16, 17, 18), (13, 14, 15)]
    basic_result = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15), (16, 17, 18)]

    def testBasicSorter(self):
        basic_sorter = BasicSorter(BuiltInSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

        basic_sorter = BasicSorter(RedSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

        basic_sorter = BasicSorter(GreenSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

        basic_sorter = BasicSorter(BlueSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

        basic_sorter = BasicSorter(BrightnessSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

        basic_sorter = BasicSorter(AvgSort)
        self.assertEqual(basic_sorter.sort_pixels(self.basic_pixels), self.basic_result)

    row_pixels = [(4, 5, 6), (7, 8, 9), (1, 2, 3), (13, 14, 15), (10, 11, 12),
                  (7, 8, 9), (4, 5, 6), (10, 11, 12), (1, 2, 3), (13, 14, 15)]
    row_result = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15),
                  (13, 14, 15), (10, 11, 12), (7, 8, 9), (4, 5, 6), (1, 2, 3)]

    def testRowSorter(self):
        row_sorter = RowSorter(5, 2, RedSort, 0)
        self.assertEqual(row_sorter.sort_pixels(self.row_pixels)[:5], self.row_result[:5])

        row_sorter = RowSorter(5, 2, RedSort, 1, True)
        self.assertEqual(row_sorter.sort_pixels(self.row_pixels)[5:], self.row_result[5:])
