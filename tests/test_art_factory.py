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
        self.assertEqual(int(len(sort_criteria.all_criteria) / batch_size) + 1, actual.qsize())

        def make(criteria: str) -> SortingImage:
            return SortingImage(images[0], BasicSorter(), criteria)

        expected = [make("BuiltIn"), make("Red"), make("Green"), make("Blue"), make("Brightness"), make("Average"),
                    make("Hue"), make("Saturation"), make("Lightness"), make("HalfThresholdBuiltIn"),
                    make("HalfThresholdRed"), make("HalfThresholdGreen"), make("HalfThresholdBlue"),
                    make("HalfThresholdBrightness"), make("HalfThresholdAverage"), make("HalfThresholdHue"),
                    make("HalfThresholdSaturation"), make("HalfThresholdLightness")]

        for _ in range(5):
            actual_batch = actual.get()
            for sorting_image in actual_batch:
                self.assertTrue(sorting_image in expected,
                                "\nsorting_image: {}\nactual_batch: {}".format(sorting_image,
                                                                               list(map(str, actual_batch))))
        self.assertTrue(actual.empty())

    def testRunSortersOnDirectory(self):
        expected_files = ['BasicSorterHalfThresholdGreen.jpg', 'BasicSorterHalfThresholdRed.jpg', 'BasicSorterHue.jpg',
                          'BasicSorterRed.jpg', 'BasicSorterBuiltIn.jpg', 'BasicSorterHalfThresholdLightness.jpg',
                          'BasicSorterAverage.jpg', 'BasicSorterBrightness.jpg',
                          'BasicSorterHalfThresholdBrightness.jpg', 'BasicSorterHalfThresholdBuiltIn.jpg',
                          'BasicSorterGreen.jpg', 'BasicSorterHalfThresholdBlue.jpg',
                          'BasicSorterHalfThresholdAverage.jpg', 'BasicSorterBlue.jpg',
                          'BasicSorterHalfThresholdHue.jpg', 'BasicSorterLightness.jpg',
                          'BasicSorterHalfThresholdSaturation.jpg', 'BasicSorterSaturation.jpg']

        path = "./runSortersOnDirectory"
        image_name = "hello"

        try:
            os.mkdir(path)
            create_test_image(os.path.join(path, image_name + ".jpg"), 1, 1, [1], "RGB")

            run_sorters_on_directory(path, [BasicSorter()])

            expected_path = os.path.join(path, image_name)
            self.assertTrue(os.path.exists(expected_path))

            actual_files = os.listdir(expected_path)
            self.assertEqual(18, len(actual_files))
            for file in expected_files:
                self.assertTrue(file in actual_files,
                                "{} not in actual_files\nactual_files: {}".format(file, actual_files))
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
