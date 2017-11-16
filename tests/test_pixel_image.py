import unittest

from pixel_sorting.helper import PixelImage


class PixelImageTest(unittest.TestCase):
    def testGetExtension(self):
        self.assertEqual(PixelImage(0, 0, [], "hello.jpg", 0).get_extension(), "jpg")
