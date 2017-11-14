import sort_criteria
from helper import get_pixels


class PixelSorter(object):
    def __init__(self, name, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False):
        self.name = name
        self.img_width = img_width
        self.img_height = img_height
        self.criteria = criteria
        self.reverse = reverse

    def to_string(self):
        return self.name

    def copy(self):
        pass

    def sort_pixels(self, pixels):
        pass

    def sort_image(self, img):
        return self.sort_pixels(get_pixels(img))


class BasicSorter(PixelSorter):
    def __init__(self, criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("BasicSorter", criteria=criteria, reverse=reverse)

    def copy(self):
        return BasicSorter(self.criteria, self.reverse)

    def sort_pixels(self, pixels):
        pixels.sort(key=self.criteria, reverse=self.reverse)
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__("Inverter")

    def copy(self):
        return Inverter()

    def sort_pixels(self, pixels):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels
