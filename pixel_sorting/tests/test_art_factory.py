import os
import shutil
from time import sleep
from unittest import TestCase

from pixel_sorting.art_factory import *


class ArtFactoryTest(TestCase):
    image_tests = [("image.png", True), ("image.PnG", True), ("image.PNG", True), ("image.JPG", True),
                   ("image.jpg", True), ("image.pn", False), ("imagepng", False), ("image,jpg", False)]

    def testIsImageFile(self):
        for test in self.image_tests:
            self.assertEqual(is_image_file(test[0]), test[1])

    test_directory = "./pixel_sorting/tests/images/"
    test_images = ["hello.png", "What.Up", "test.jpg", "hey/here.png"]
    expected_image_paths = [test_directory + "test.jpg", test_directory + "hello.png", test_directory + "hey/here.png"]

    def testGetImageFiles(self):
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
        for file in self.test_images:
            if not os.path.exists(self.test_directory + file):
                k = file.rfind("/")
                if k != -1:
                    os.makedirs(self.test_directory + file[:k])
            open(self.test_directory + file, 'w+').close()

        image_files = get_image_files(self.test_directory)
        for image in self.expected_image_paths:
            self.assertTrue(image in image_files)

        shutil.rmtree(self.test_directory)

    def testGetExtension(self):
        self.assertEqual(get_extension("hello.jpg"), "jpg")

    def testRemoveExtension(self):
        self.assertEqual(remove_extension("hello.jpg"), "hello")
        self.assertEqual(remove_extension("./hello.jpg"), "./hello")

    expected_sorters = ["BasicSorter", "Inverter", "AlternatingRowSorter1", "AlternatingRowSorter10",
                        "AlternatingRowSorter100", "AlternatingColumnSorter1", "AlternatingColumnSorter10",
                        "AlternatingColumnSorter100", "DiamondSorter", "CircleSorter", "CheckerBoardSorter"]
    expected_criteria = ["Average", "Blue", "Brightness", "BuiltIn", "Green", "Hue", "Lightness", "Red", "Saturation"]

    def testApplySortersToImage(self):
        apply_all_sorters_to_image("./pixel_sorting/tests/test_image.png")
        image_folder = "./pixel_sorting/tests/test_image_generated/"
        try:
            self.assertTrue(os.path.exists(image_folder))
            num_files = len(
                [name for name in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, name))])
            self.assertEqual(num_files, (len(self.expected_sorters) - 1) * len(self.expected_criteria) + 1)
            for sorter in self.expected_sorters:
                for criteria in self.expected_criteria:
                    image_path = image_folder + sorter + criteria + ".png"
                    if sorter == "Inverter":
                        image_path = image_folder + sorter + ".png"
                    self.assertTrue(os.path.exists(image_path), "Image file " + image_path + " does not exist.")
        finally:
            shutil.rmtree(image_folder)

    def testApplySortersToDir(self):
        test_directory = "./pixel_sorting/tests/"
        apply_all_sorters_to_dir(test_directory)
        try:
            test_dir_1 = test_directory + "test_image_generated/"
            self.assertTrue(os.path.exists(test_dir_1))
            num_files = len([name for name in os.listdir(test_dir_1) if
                             os.path.isfile(os.path.join(test_dir_1, name))])
            self.assertEqual(num_files, (len(self.expected_sorters) - 1) * len(self.expected_criteria) + 1)
            for sorter in self.expected_sorters:
                for criteria in self.expected_criteria:
                    image_path = test_dir_1 + sorter + criteria + ".png"
                    if sorter == "Inverter":
                        image_path = test_dir_1 + sorter + ".png"
                    self.assertTrue(os.path.exists(image_path), "Image file " + image_path + " does not exist.")

            test_dir_2 = test_directory + "test_image_sorters_generated/"
            self.assertTrue(os.path.exists("./pixel_sorting/tests/test_image_sorters_generated"))
            num_files = len([name for name in os.listdir(test_dir_2) if
                             os.path.isfile(os.path.join(test_dir_2, name))])
            self.assertEqual(num_files, (len(self.expected_sorters) - 1) * len(self.expected_criteria) + 1)
            for sorter in self.expected_sorters:
                for criteria in self.expected_criteria:
                    image_path = test_dir_2 + sorter + criteria + ".jpg"
                    if sorter == "Inverter":
                        image_path = test_dir_2 + sorter + ".jpg"
                    self.assertTrue(os.path.exists(image_path), "Image file " + image_path + " does not exist.")

        finally:
            shutil.rmtree("./pixel_sorting/tests/test_image_generated")
            shutil.rmtree("./pixel_sorting/tests/test_image_sorters_generated")

    def testIsGeneratedImage(self):
        self.assertTrue(is_generated_image("/generated_some_folder/some_image.jpg"))
        self.assertFalse(is_generated_image("./res/city_folder/city.png"))
