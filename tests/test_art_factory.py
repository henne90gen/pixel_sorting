import logging
import os
import shutil
import unittest

from PIL import Image
from multiprocessing.dummy.connection import Connection

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.art_factory import create_batch_queue, process_batch, get_all_sorters, run_sorters_on_directory
from pixel_sorting.helper import PixelImage, SortingImage
from pixel_sorting.sorters.basic import BasicSorter
from tests.test_helper import assert_generated_directory, create_test_image

logging.getLogger().setLevel(logging.ERROR)


class PipeMock:
    def __init__(self, tester: unittest.TestCase, skipped: int = 0, processed: int = 0, errors: int = 0):
        self.tester = tester
        self.skipped = skipped
        self.processed = processed
        self.errors = errors

    def send(self, obj):
        self.tester.assertEqual(self.skipped, obj["skipped"])
        self.tester.assertEqual(self.processed, obj["processed"])
        self.tester.assertEqual(self.errors, obj["errors"])


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

    def testProcessBatch(self):
        filename = "./test.jpg"
        create_test_image(filename, 1, 1, [1], "RGB")

        image = PixelImage(1, 1, filename, "RGB")
        batch = [SortingImage(image, BasicSorter(), "BuiltIn"), SortingImage(image, BasicSorter(), "Red"),
                 SortingImage(image, BasicSorter(), "Green"), SortingImage(image, BasicSorter(), "Blue")]

        try:
            # noinspection PyTypeChecker
            process_batch(batch, PipeMock(self, 0, 4, 0))

            self.assertTrue(os.path.exists('./test'))
            self.assertTrue(os.path.exists('./test/BasicSorterBuiltIn.jpg'))
            self.assertTrue(os.path.exists('./test/BasicSorterRed.jpg'))
            self.assertTrue(os.path.exists('./test/BasicSorterGreen.jpg'))
            self.assertTrue(os.path.exists('./test/BasicSorterBlue.jpg'))
        finally:
            shutil.rmtree("./test")
            os.remove("./test.jpg")

    def testCreateBatchQueue(self):
        images = [PixelImage(0, 0, "test.jpg", "")]
        sorters = [BasicSorter()]
        batch_size = 4
        actual = create_batch_queue(images, sorters, batch_size)
        self.assertEqual(int(len(sort_criteria.all_criteria) / batch_size), actual.qsize())

        def make(criteria: str) -> SortingImage:
            return SortingImage(images[0], BasicSorter(), criteria)

        expected = [[make("BuiltIn"), make("Red"), make("Green"), make("Blue")],
                    [make("Brightness"), make("Average"), make("Hue"), make("Saturation")],
                    [make("Lightness"), make("HalfThresholdBuiltIn"), make("HalfThresholdRed"),
                     make("HalfThresholdGreen")],
                    [make("HalfThresholdBlue"), make("HalfThresholdBrightness"), make("HalfThresholdAverage"),
                     make("HalfThresholdHue")]]

        for batch in expected:
            actual_batch = actual.get()
            for index, sorting_image in enumerate(batch):
                self.assertEqual(sorting_image, actual_batch[index])

        self.assertTrue(actual.empty())

    def testRunSortersOnDirectory(self):
        expected_files = ['BasicSorterHue.jpg', 'BasicSorterRed.jpg', 'BasicSorterBuiltIn.jpg',
                          'BasicSorterAverage.jpg', 'BasicSorterBrightness.jpg', 'BasicSorterHalfThresholdBuiltIn.jpg',
                          'BasicSorterGreen.jpg', 'BasicSorterBlue.jpg', 'BasicSorterLightness.jpg',
                          'BasicSorterSaturation.jpg']
        path = "./runSortersOnDirectory"
        image_name = "hello"

        try:
            os.mkdir(path)
            create_test_image(os.path.join(path, image_name + ".jpg"), 1, 1, [1], "RGB")

            run_sorters_on_directory(path, [BasicSorter()])

            expected_path = os.path.join(path, image_name)
            self.assertTrue(os.path.exists(expected_path))

            actual_files = os.listdir(expected_path)
            self.assertEqual(10, len(actual_files))
            print(actual_files)
            for file in expected_files:
                print(file)
                self.assertTrue(file in actual_files)
        finally:
            shutil.rmtree(path)

    def testGetAllSorters(self):
        expected = ["BasicSorter", "Inverter", "AlternatingRowSorter1", "AlternatingRowSorter10",
                    "AlternatingRowSorter100", "AlternatingColumnSorter1", "AlternatingColumnSorter10",
                    "AlternatingColumnSorter100", "DiamondSorter", "CircleSorter", "CheckerBoardSorter8x8(BasicSorter)",
                    "CheckerBoardSorter8x8(AlternatingRowSorter1)", "CheckerBoardSorter8x8(AlternatingRowSorter10)",
                    "CheckerBoardSorter8x8(AlternatingRowSorter100)", "CheckerBoardSorter8x8(AlternatingColumnSorter1)",
                    "CheckerBoardSorter8x8(AlternatingColumnSorter10)",
                    "CheckerBoardSorter8x8(AlternatingColumnSorter100)", "CheckerBoardSorter8x8(DiamondSorter)",
                    "CheckerBoardSorter8x8(CircleSorter)"]
        actual = get_all_sorters()
        actual = list(map(lambda s: s.name, actual))
        self.assertEqual(len(expected), len(actual))
        for index, sorter in enumerate(expected):
            self.assertEqual(sorter, actual[index])
