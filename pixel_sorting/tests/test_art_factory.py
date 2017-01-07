import os
import shutil
from unittest import TestCase

from pixel_sorting import art_factory as af


class ArtFactoryTest(TestCase):
    image_tests = [("image.png", True), ("image.PnG", True), ("image.PNG", True), ("image.JPG", True),
                   ("image.jpg", True), ("image.pn", False), ("imagepng", False), ("image,jpg", False)]

    def testIsImageFile(self):
        for test in self.image_tests:
            self.assertEqual(af.is_image_file(test[0]), test[1])

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

        image_files = af.get_image_files(self.test_directory)
        for image in self.expected_image_paths:
            self.assertTrue(image in image_files)

        shutil.rmtree(self.test_directory)

    def testGetExtension(self):
        self.assertEqual(af.get_extension("hello.jpg"), "jpg")

    def testRemoveExtension(self):
        self.assertEqual(af.remove_extension("hello.jpg"), "hello")
        self.assertEqual(af.remove_extension("./hello.jpg"), "./hello")

    expected_sorters = ["BasicSorter", "Inverter", "AlternatingRowSorter", "AlternatingColumnSorter", "DiamondSorter",
                        "CircleSorter"]
    expected_criteria = ["Average", "Blue", "Brightness", "BuiltIn", "Green", "Hue", "Lightness", "Red", "Saturation"]

    def testApplySorterToImage(self):
        af.apply_sorters_to_image("./pixel_sorting/tests/test_image.png")
        image_folder = "./pixel_sorting/tests/test_image_folder/"

        self.assertTrue(os.path.exists(image_folder))
        num_files = len([name for name in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, name))])
        self.assertEqual(num_files, (len(self.expected_sorters) - 1) * len(self.expected_criteria) + 1)
        for sorter in self.expected_sorters:
            for criteria in self.expected_criteria:
                image_path = image_folder + sorter + criteria + ".png"
                if sorter == "Inverter":
                    image_path = image_folder + sorter + ".png"
                self.assertTrue(os.path.exists(image_path), "Image file " + image_path + " does not exist.")

        shutil.rmtree(image_folder)
