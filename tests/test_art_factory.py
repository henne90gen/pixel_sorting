import shutil
import unittest

from pixel_sorting.art_factory import *
from tests.test_helper import assert_generated_directory, get_expected_files_per_image, create_test_image


class ArtFactoryTest(unittest.TestCase):
    image_tests = [("image.png", True), ("image.PnG", True), ("image.PNG", True), ("image.JPG", True),
                   ("image.jpg", True), ("image.pn", False), ("imagepng", False), ("image,jpg", False)]

    def testIsImageFile(self):
        for test in self.image_tests:
            self.assertEqual(is_image_file(test[0]), test[1])

    test_directory = "./images/"
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

    expected_sorters = ['BasicSorter', 'Inverter', 'AlternatingRowSorter1', 'AlternatingRowSorter10',
                        'AlternatingRowSorter100', 'AlternatingColumnSorter1', 'AlternatingColumnSorter10',
                        'AlternatingColumnSorter100', 'DiamondSorter', 'CircleSorter', 'CheckerBoardSorterBasicSorter',
                        'CheckerBoardSorterAlternatingRowSorter', 'CheckerBoardSorterAlternatingColumnSorter',
                        'CheckerBoardSorterDiamondSorter', 'CheckerBoardSorterCircleSorter',
                        'CheckerBoardSorterCheckerBoardSorter']

    expected_criteria = ["Average", "Blue", "Brightness", "BuiltIn", "Green", "Hue", "Lightness", "Red", "Saturation",
                         "HalfThresholdAverage", "HalfThresholdBlue", "HalfThresholdBrightness", "HalfThresholdBuiltIn",
                         "HalfThresholdGreen", "HalfThresholdHue", "HalfThresholdLightness", "HalfThresholdRed",
                         "HalfThresholdSaturation"]

    def testApplySortersToImage(self):
        art_factory_image = "./applySortersToImage.png"
        create_test_image(art_factory_image, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        image_folder = "./applySortersToImage_generated/"

        try:
            apply_all_sorters_to_image(art_factory_image)
            assert_generated_directory(self, image_folder, self.expected_sorters, self.expected_criteria, ".png")
        finally:
            os.remove(art_factory_image)
            shutil.rmtree(image_folder)

    def testApplySortersToDir(self):
        test_directory = "./applySortersToDir/"
        os.mkdir(test_directory)

        test_img1 = "img1.png"
        create_test_image(test_directory + test_img1, 5, 5, [(i, i, i) for i in range(25)], "RGB")

        test_img2 = "img2.jpg"
        create_test_image(test_directory + test_img2, 5, 5, [(i, i, i) for i in range(25)], "RGB")

        try:
            apply_all_sorters_to_dir(test_directory)

            test_dir_1 = test_directory + "img1_generated/"
            assert_generated_directory(self, test_dir_1, self.expected_sorters, self.expected_criteria, ".png")

            test_dir_2 = test_directory + "img2_generated/"
            assert_generated_directory(self, test_dir_2, self.expected_sorters, self.expected_criteria, ".jpg")
        finally:
            shutil.rmtree(test_directory)

    def testIsGeneratedImage(self):
        self.assertTrue(is_generated_image("/generated_some_folder/some_image.jpg"))
        self.assertFalse(is_generated_image("./res/city_folder/city.png"))

    def testApplySorterToImage(self):
        image_name = "./applySorterToImage.png"
        create_test_image(image_name, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        image = Image.open(image_name)
        sorter_template = BasicSorter()
        criteria = "BuiltIn"
        extension = ".png"
        test_directory = "./applySorterToImage_generated/"
        path_to_image = get_generated_image_path(test_directory, sorter_template,
                                                 criteria, extension)
        argument = [path_to_image, sorter_template, criteria, image.size[0], image.size[1], image.mode,
                    get_pixels(image)]
        os.mkdir(test_directory)

        try:
            self.assertEqual(apply_sorter_to_image(argument), True)
            self.assertEqual(apply_sorter_to_image(argument), False)
        finally:
            os.remove(image_name)
            shutil.rmtree(test_directory)

    def testApplyFavoriteToImage(self):
        test_image = "./applyFavoriteToImage.png"
        pixels = [(i, i, i) for i in range(25)]
        create_test_image(test_image, 5, 5, pixels, "RGB")
        try:
            self.assertEqual(apply_favorite_sorters_to_image(test_image), 90)
        finally:
            shutil.rmtree("./applyFavoriteToImage_generated")
            os.remove(test_image)

    def testApplyFavoriteToDir(self):
        test_dir = "./applyFavoriteToDir"
        os.mkdir(test_dir)

        test_image1 = "./applyFavoriteToDir/applyFavoriteToDir1.png"
        test_image2 = "./applyFavoriteToDir/applyFavoriteToDir2.png"
        pixels = [(i, i, i) for i in range(25)]
        create_test_image(test_image1, 5, 5, pixels, "RGB")
        create_test_image(test_image2, 5, 5, pixels, "RGB")
        try:
            self.assertEqual(apply_favorite_sorters_to_dir(test_dir), 180)
        finally:
            shutil.rmtree(test_dir)
