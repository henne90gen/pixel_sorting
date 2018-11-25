import logging
import os
import shutil
import unittest

import cv2
import numpy as np

from pixel_sorting.helper import remove_extension, PixelImage, is_image_file, is_generated_image, get_images, \
    SortingImage, create_pixel_image, save_to_image, get_pixels, Timer
from pixel_sorting.sorters.basic import BasicSorter

logging.getLogger().setLevel(logging.ERROR)


class PixelImageTest(unittest.TestCase):
    def setUp(self):
        self.image = PixelImage(0, 0, "hello.jpg")

    def testNotEquals(self):
        self.assertFalse(self.image == Timer(logging.getLogger(), ""))

    def testToString(self):
        expected = "hello.jpg (0x0)"
        actual = str(self.image)
        self.assertEqual(expected, actual)

    def testGetExtension(self):
        expected = "jpg"
        actual = self.image.get_extension()
        self.assertEqual(expected, actual)

    def testCreateDirectory(self):
        expected_path = "./hello"
        self.image.create_directory()
        self.assertTrue(os.path.exists(expected_path))
        shutil.rmtree(expected_path)

    def testLoadPixels(self):
        expected = [[(1, 2, 4), (1, 2, 4), (1, 2, 4)], [
            (1, 2, 4), (1, 2, 4), (1, 2, 4)], [(1, 2, 4), (1, 2, 4), (1, 2, 4)]]
        filename = "test.jpg"
        save_to_image(0, 0, "", expected, filename)
        image = PixelImage(3, 3, filename)
        actual = image.load_pixels()
        print(actual)
        print(expected)
        for i in range(len(np.array(expected).flat)):
            self.assertEqual(np.array(expected).flat[i], actual.flat[i])
        os.remove(filename)


class PixelImageMock(PixelImage):
    def __init__(self, file_path="", pixels=None):
        super().__init__(0, 0, file_path)
        if pixels is None:
            pixels = []
        self.pixels = pixels

    def load_pixels(self):
        return self.pixels


class SortingImageTest(unittest.TestCase):
    def setUp(self):
        self.sorting_image_path = "./test/BasicSorterBuiltIn.jpg"
        test_image_path = "./test.jpg"
        pixel_image = PixelImageMock(test_image_path)
        sorter = BasicSorter()
        self.sorting_image = SortingImage(pixel_image, sorter, "BuiltIn")

    def testEquals(self):
        pixel_image = PixelImage(0, 0, "./test.jpg")
        image = SortingImage(pixel_image, BasicSorter(), "BuiltIn")
        other = SortingImage(pixel_image, BasicSorter(), "BuiltIn")
        self.assertTrue(image == other)
        self.assertTrue(image != pixel_image)

    def testToString(self):
        self.assertEqual(
            "./test.jpg (0x0): BasicSorter BuiltIn", str(self.sorting_image))

    def testGetNewPath(self):
        expected = self.sorting_image_path
        actual = self.sorting_image.get_new_path()
        self.assertEqual(expected, actual)

    def testSort(self):
        self.sorting_image.pixel_image = PixelImageMock(
            "test.jpg", [5, 3, 4, 1, 2])
        expected = [1, 2, 3, 4, 5]
        self.sorting_image.sort()
        actual = self.sorting_image.pixels
        self.assertEqual(expected, actual)

    def testSave(self):
        self.sorting_image.pixels = [[0, 1, 2], [2, 3, 4]]
        self.sorting_image.pixel_image.width = 2
        self.sorting_image.pixel_image.height = 2
        self.sorting_image.save()
        self.assertTrue(os.path.exists(self.sorting_image_path))
        shutil.rmtree('test')


class TimerTest(unittest.TestCase):
    def testTimer(self):
        expected = ["Starting task 'testTask'",
                    "Task 'testTask' finished after 0.000s"]

        class LoggerMock(logging.Logger):
            index = 0

            def info(this, msg, **kwargs):
                self.assertEqual(expected[this.index], msg)
                this.index += 1

        with Timer(LoggerMock("test"), "testTask"):
            pass


class HelperTest(unittest.TestCase):
    def setUp(self):
        self.helper_png = "./helper.png"
        pixels = [[i*5+j for j in range(5)] for i in range(5)]
        create_test_image(self.helper_png, pixels)

    def tearDown(self):
        os.remove(self.helper_png)

    def testRemoveExtension(self):
        self.assertEqual("hello", remove_extension("hello.jpg"))
        self.assertEqual("./hello", remove_extension("./hello.jpg"))

    def testIsImageFile(self):
        image_tests = [("image.png", True), ("image.PnG", True), ("image.PNG", True), ("image.JPG", True),
                       ("image.jpg", True), ("image.pn", False), ("imagepng", False), ("image,jpg", False)]
        for test in image_tests:
            self.assertEqual(is_image_file(test[0]), test[1])

    def testIsGeneratedImage(self):
        self.assertTrue(is_generated_image(
            "/generated_some_folder/some_image.jpg"))
        self.assertFalse(is_generated_image("./res/city_folder/city.png"))

    def testCreatePixelImage(self):
        expected = PixelImage(5, 5, "./helper.png")
        actual = create_pixel_image(self.helper_png)
        self.assertEqual(expected, actual)

    def testGetImages(self):
        test_directory = "./images"
        test_images = ["hello.png", "What.Up", "test.jpg", "hey/here.png"]
        expected_images = [PixelImage(
            1, 1, "./images/test.jpg"), PixelImage(1, 1, "./images/hello.png")]

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
                    self.fail(
                        "Find out what needs to be done, when we reach this point")
                else:
                    open(new_path, "w").close()

            images = get_images(test_directory)
            self.assertEqual(len(expected_images), len(images))

            for index, image in enumerate(expected_images):
                self.assertTrue(image in expected_images)
        finally:
            shutil.rmtree(test_directory)

    def testSaveToImage(self):
        filename = "./helper.png"
        expected = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0),
                    (5, 0, 0), (6, 0, 0), (7, 0, 0), (8, 0, 0), (9, 0, 0)]
        save_to_image(3, 3, "RGB", expected, filename)
        self.assertTrue(os.path.exists(filename))

    def testGetPixels(self):
        filename = "./helper.png"
        expected = [[(1, 0, 0), (2, 0, 0), (3, 0, 0)], [(4, 0, 0),
                                                        (5, 0, 0), (6, 0, 0)], [(7, 0, 0), (8, 0, 0), (9, 0, 0)]]
        save_to_image(3, 3, "RGB", expected, filename)
        actual = cv2.imread(filename)
        self.assertEqual(expected, actual)


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

    circle_sorter.draw_circle(
        test_pixels, pixel_source, pixel_set, 0, 5, 5, radius)
    tester.assertEqual(test_pixels, expected_result)


def create_test_image(path: str, test_pixels: list):
    pixels = np.array(test_pixels)
    cv2.imwrite(path, pixels)
