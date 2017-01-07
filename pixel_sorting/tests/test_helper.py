import unittest
from pixel_sorting import *


class HelperTest(unittest.TestCase):
    def testSaveToCopy(self):
        path = "./pixel_sorting/tests/"
        filename = "test_image.png"
        img = Image.open(path + filename)
        pixels = get_pixels(img)
        save_to_copy(img, pixels, path + "copy_" + filename)
        self.assertTrue(os.path.exists(path + filename), "Original file doesn't exist any more.")
        self.assertTrue(os.path.exists(path + "copy_" + filename), "No copy was created.")


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
