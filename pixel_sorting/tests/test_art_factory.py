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

        self.assertListEqual(af.get_image_files(self.test_directory), self.expected_image_paths)

        shutil.rmtree(self.test_directory)
