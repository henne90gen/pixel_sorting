"""
This module defines some very basic pixel sorting algorithms
"""

from pixel_sorting import sort_criteria


class PixelSorter:
    """
    Base class for all pixel sorters
    """

    def __init__(self, name, reverse=False):
        self.name = name
        self.reverse = reverse

    def __str__(self):
        return self.name

    def sort_pixels(self, pixels: list, img_width: int, img_height: int,
                    criteria=sort_criteria.built_in()) -> list:
        """
        Abstract method that has to be implemented by every pixel sorter
        """
        return pixels


class BasicSorter(PixelSorter):
    """
    Sorts pixels using the default python sorting of lists with the given criteria
    """

    def __init__(self, reverse=False):
        super().__init__("BasicSorter", reverse=reverse)

    def sort_pixels(self, pixels: list, img_width: int, img_height: int,
                    criteria=sort_criteria.built_in()) -> list:
        pixels.sort(key=criteria, reverse=self.reverse)
        return pixels


class Inverter(PixelSorter):
    """
    Inverts the image
    """

    def __init__(self):
        super().__init__("Inverter")

    def sort_pixels(self, pixels: list, img_width: int, img_height: int,
                    criteria=sort_criteria.built_in()) -> list:
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels
