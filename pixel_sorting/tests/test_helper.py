import os
import unittest

from pixel_sorting.helper import *


class HelperTest(unittest.TestCase):
    def testSaveToCopy(self):
        filename = "test_image.png"
        img = Image.open(filename)
        pixels = get_pixels(img)
        save_to_copy(img, pixels, "copy_" + filename)
        self.assertTrue(os.path.exists(filename), "Original file doesn't exist any more.")
        self.assertTrue(os.path.exists("copy_" + filename), "No copy was created.")
