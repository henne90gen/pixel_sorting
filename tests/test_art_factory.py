import logging
import os
import shutil
import unittest

from PIL import Image

from pixel_sorting.sorters.basic import BasicSorter
from tests.test_helper import assert_generated_directory, create_test_image

logging.getLogger().setLevel(logging.ERROR)


class ArtFactoryTest(unittest.TestCase):
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

    @unittest.skip("Make new art_factory tests go green")
    def testApplySortersToImage(self):
        art_factory_image = "./applySortersToImage.png"
        create_test_image(art_factory_image, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        image_folder = "./applySortersToImage/"

        try:
            # apply_all_sorters_to_image(art_factory_image)
            assert_generated_directory(self, image_folder, self.expected_sorters, self.expected_criteria, ".png")
        finally:
            os.remove(art_factory_image)
            shutil.rmtree(image_folder)

    @unittest.skip("Make new art_factory tests go green")
    def testApplySortersToDir(self):
        test_directory = "./applySortersToDir/"
        os.mkdir(test_directory)

        test_img1 = "img1.png"
        create_test_image(test_directory + test_img1, 5, 5, [(i, i, i) for i in range(25)], "RGB")

        test_img2 = "img2.jpg"
        create_test_image(test_directory + test_img2, 5, 5, [(i, i, i) for i in range(25)], "RGB")

        try:
            # apply_all_sorters_to_dir(test_directory)

            test_dir_1 = test_directory + "img1/"
            assert_generated_directory(self, test_dir_1, self.expected_sorters, self.expected_criteria, ".png")

            test_dir_2 = test_directory + "img2/"
            assert_generated_directory(self, test_dir_2, self.expected_sorters, self.expected_criteria, ".jpg")
        finally:
            shutil.rmtree(test_directory)

    @unittest.skip("Make new art_factory tests go green")
    def testApplySorterToImage(self):
        image_name = "./applySorterToImage.png"
        create_test_image(image_name, 5, 5, [(i, i, i) for i in range(25)], "RGB")
        image = Image.open(image_name)
        sorter_template = BasicSorter()
        criteria = "BuiltIn"
        extension = ".png"
        test_directory = "./applySorterToImage_generated/"
        # path_to_image = get_generated_image_path(test_directory, sorter_template,
        #                                          criteria, extension)
        # argument = [path_to_image, sorter_template, criteria, image.size[0], image.size[1], image.mode,
        #             get_pixels(image)]
        os.mkdir(test_directory)

        try:
            # self.assertEqual(apply_sorter_to_image(argument), True)
            # self.assertEqual(apply_sorter_to_image(argument), False)
            pass
        finally:
            os.remove(image_name)
            shutil.rmtree(test_directory)

    @unittest.skip("Make new art_factory tests go green")
    def testApplyFavoriteToImage(self):
        test_image = "./applyFavoriteToImage.png"
        pixels = [(i, i, i) for i in range(25)]
        create_test_image(test_image, 5, 5, pixels, "RGB")
        try:
            # self.assertEqual(apply_favorite_sorters_to_image(test_image), 90)
            pass
        finally:
            shutil.rmtree("./applyFavoriteToImage")
            os.remove(test_image)

    @unittest.skip("Make new art_factory tests go green")
    def testApplyFavoriteToDir(self):
        test_dir = "./applyFavoriteToDir"
        os.mkdir(test_dir)

        test_image1 = "./applyFavoriteToDir/applyFavoriteToDir1.png"
        test_image2 = "./applyFavoriteToDir/applyFavoriteToDir2.png"
        pixels = [(i, i, i) for i in range(25)]
        create_test_image(test_image1, 5, 5, pixels, "RGB")
        create_test_image(test_image2, 5, 5, pixels, "RGB")
        try:
            # self.assertEqual(apply_favorite_sorters_to_dir(test_dir), 180)
            pass
        finally:
            shutil.rmtree(test_dir)

    @unittest.skip("Implement this")
    def testProcessBatch(self):
        pass

    @unittest.skip("Implement this")
    def testCreateBatchQueue(self):
        pass

    @unittest.skip("Implement this")
    def testRunSortersOnDirectory(self):
        pass

    @unittest.skip("Implement this")
    def testGetAllSorters(self):
        pass
