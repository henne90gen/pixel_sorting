import logging
import os
import shutil
import unittest

from PIL import Image

from pixel_sorting.helper import remove_extension, PixelImage, is_image_file, is_generated_image, get_images
from pixel_sorting.sorters.basic import PixelSorter

helper_png = "./helper.png"

logging.getLogger().setLevel(logging.ERROR)


class PixelImageTest(unittest.TestCase):
    def testGetExtension(self):
        try:
            self.assertEqual(PixelImage(0, 0, [], "hello.jpg", 0).get_extension(), "jpg")
        finally:
            os.rmdir("./hello")

    def testCreateDirectory(self):
        pass


@unittest.skip("Implement this")
class SortingImageTest(unittest.TestCase):
    def testGetNewPath(self):
        pass

    def testSort(self):
        pass

    def testSave(self):
        pass


@unittest.skip("Implement this")
class TimerTest(unittest.TestCase):
    def test(self):
        pass


class HelperTest(unittest.TestCase):
    def setUp(self):
        create_test_image(helper_png, 5, 5, [(i, i, i) for i in range(25)], "RGB")

    def tearDown(self):
        os.remove(helper_png)

    def testRemoveExtension(self):
        self.assertEqual("hello", remove_extension("hello.jpg"))
        self.assertEqual("./hello", remove_extension("./hello.jpg"))

    def testIsImageFile(self):
        image_tests = [("image.png", True), ("image.PnG", True), ("image.PNG", True), ("image.JPG", True),
                       ("image.jpg", True), ("image.pn", False), ("imagepng", False), ("image,jpg", False)]
        for test in image_tests:
            self.assertEqual(is_image_file(test[0]), test[1])

    def testIsGeneratedImage(self):
        self.assertTrue(is_generated_image("/generated_some_folder/some_image.jpg"))
        self.assertFalse(is_generated_image("./res/city_folder/city.png"))

    @unittest.skip("Implement this")
    def testGetGeneratedImagePath(self):
        self.assertTrue(False)

    @unittest.skip("Implement this")
    def testCreatePixelImage(self):
        self.assertTrue(False)

    @unittest.skip("Fix this")
    def testGetImages(self):
        test_directory = "./images"
        test_images = ["hello.png", "What.Up", "test.jpg", "hey/here.png"]
        expected_images = [PixelImage(0, 0, [0], "./images/hello.png", "1"),
                           PixelImage(0, 0, [0], "./images/test.jpg", "1")]

        try:
            if not os.path.exists(test_directory):
                os.makedirs(test_directory)

            for file in test_images:
                new_path = os.path.join(test_directory, file)

                if not os.path.exists(new_path):
                    k = file.rfind("/")
                    if k != -1:
                        os.makedirs(os.path.join(test_directory, file[:k]))

                if is_image_file(file):
                    new_image = Image.new("1", (1, 1))
                    new_image.putdata([0])
                    new_image.save(new_path)
                    new_image.close()
                else:
                    open(new_path, "w").close()

            images = get_images(test_directory)
            self.assertEqual(len(expected_images), len(images))
            for image in expected_images:
                self.assertTrue(image in images)
        finally:
            shutil.rmtree(test_directory)

    @unittest.skip("Implement this")
    def testSaveToImage(self):
        self.assertTrue(False)

    @unittest.skip("Implement this")
    def testGetPixels(self):
        self.assertTrue(False)

    @unittest.skip("Implement this")
    def testPixelsToLinearArray(self):
        self.assertTrue(False)


def execute_sorter(tester, sorter: PixelSorter, input_pixels, expected_result):
    test_pixels = [p for p in input_pixels]
    tester.assertEqual(sorter.sort_pixels(test_pixels), expected_result)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_circle(tester, circle_sorter, expected_result, radius, circle_pixels, pixel_source):
    test_pixels = [p for p in circle_pixels]

    # Copy from CircleSorter, this is specific for a 5x5 grid
    pixel_set = []
    x_offset = 0
    y_offset = 0
    if 5 % 2 != 0:
        x_offset = 1
    if 5 % 2 != 0:
        y_offset = 1
    center_x, center_y = circle_sorter.center(5, 5)
    for i in range(center_y + y_offset):
        temp = [False for j in range(center_x + x_offset)]
        pixel_set.append(temp)
    # end of copy

    circle_sorter.draw_circle(test_pixels, pixel_source, pixel_set, 0, 5, 5, radius)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_octants(tester, circle_sorter, x, y, expected_result, expected_index, circle_pixels, pixel_source):
    test_pixels = [p for p in circle_pixels]
    tester.assertEqual(circle_sorter.draw_octant_pixels(test_pixels, pixel_source, 0, x, y), expected_index)
    tester.assertEqual(test_pixels, expected_result)


def execute_draw_pixel(tester, circle_sorter, x, y, index, expected_result, expected_return, circle_pixels,
                       pixel_source):
    test_pixels = [p for p in circle_pixels]
    tester.assertEqual(circle_sorter.draw_pixel(test_pixels, pixel_source, index, x, y), expected_return)
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
