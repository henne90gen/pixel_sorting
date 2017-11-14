import logging
import os
import unittest

from PIL import Image

from pixel_sorting.sorters.basic import BasicSorter
from pixel_sorting.helper import get_pixels, save_to_copy, get_extension, remove_extension, get_sorter_name
from sorters.circle import CircleSorter
from sorters.column import AlternatingColumnSorter, ColumnSorter
from sorters.diamond import DiamondSorter
from sorters.row import AlternatingRowSorter, RowSorter

helper_png = "./helper.png"

logging.getLogger().setLevel(logging.ERROR)


class HelperTest(unittest.TestCase):
    def setUp(self):
        create_test_image(helper_png, 5, 5, [(i, i, i) for i in range(25)], "RGB")

    def tearDown(self):
        os.remove(helper_png)

    def testSaveToCopy(self):
        path = "./"
        filename = "helper.png"
        img = Image.open(path + filename)
        pixels = get_pixels(img)
        save_to_copy(img, pixels, path + "copy_" + filename)
        self.assertTrue(os.path.exists(path + filename), "Original file doesn't exist any more.")
        self.assertTrue(os.path.exists(path + "copy_" + filename), "No copy was created.")
        os.remove(path + "copy_" + filename)

    def testGetExtension(self):
        self.assertEqual(get_extension("hello.jpg"), "jpg")

    def testRemoveExtension(self):
        self.assertEqual("hello", remove_extension("hello.jpg"))
        self.assertEqual("./hello", remove_extension("./hello.jpg"))

    def testGetSorterName(self):
        self.assertEqual("BasicSorter", get_sorter_name(BasicSorter))
        self.assertEqual("CircleSorter", get_sorter_name(CircleSorter))
        self.assertEqual("DiamondSorter", get_sorter_name(DiamondSorter))
        self.assertEqual("RowSorter", get_sorter_name(RowSorter))
        self.assertEqual("AlternatingRowSorter", get_sorter_name(AlternatingRowSorter))
        self.assertEqual("ColumnSorter", get_sorter_name(ColumnSorter))
        self.assertEqual("AlternatingColumnSorter", get_sorter_name(AlternatingColumnSorter))


def execute_sorter(tester, sorter, input_pixels, expected_result):
    test_pixels = [p for p in input_pixels]
    tester.assertEqual(sorter.sort_pixels(test_pixels), expected_result)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_circle(tester, circle_sorter, expected_result, radius):
    test_pixels = [p for p in tester.circle_pixels]
    # Copied from CircleSorter, this is specific for a 5x5 grid
    pixel_set = []
    x_offset = 0
    y_offset = 0
    if circle_sorter.img_width % 2 != 0:
        x_offset = 1
    if circle_sorter.img_height % 2 != 0:
        y_offset = 1
    for i in range(circle_sorter.y + y_offset):
        temp = [False for j in range(circle_sorter.x + x_offset)]
        pixel_set.append(temp)
    circle_sorter.draw_circle(test_pixels, tester.pixel_source, pixel_set, 0, radius)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_octants(tester, circle_sorter, x, y, expected_result, expected_index):
    test_pixels = [p for p in tester.circle_pixels]
    tester.assertEqual(circle_sorter.draw_octant_pixels(test_pixels, tester.pixel_source, 0, x, y), expected_index)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_pixel(tester, circle_sorter, x, y, index, expected_result, expected_return):
    test_pixels = [p for p in tester.circle_pixels]
    tester.assertEqual(circle_sorter.draw_pixel(test_pixels, tester.pixel_source, index, x, y), expected_return)
    tester.assertEqual(test_pixels, expected_result)


def get_expected_files_per_image(tester):
    return (len(tester.expected_sorters) - 1) * len(tester.expected_criteria) + 1


def create_test_image(filename, width, height, pixels, mode="L"):
    img = Image.new(mode, (width, height))
    img.putdata(pixels)
    img.save(filename)


def assert_generated_directory(tester, directory, expected_sorters, expected_criteria, extension):
    num_expected_files_per_image = get_expected_files_per_image(tester)

    tester.assertTrue(os.path.exists(directory))
    num_files = len(
        [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    tester.assertEqual(num_files, num_expected_files_per_image)
    for sorter in expected_sorters:
        for criteria in expected_criteria:
            image_path = directory + sorter + criteria + extension
            if sorter == "Inverter":
                image_path = directory + sorter + extension
            tester.assertTrue(os.path.exists(image_path), "Image file " + image_path + " does not exist.")
