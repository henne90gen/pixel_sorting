import os
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
