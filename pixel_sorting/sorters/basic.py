import pixel_sorting.sort_criteria as sort_criteria


class PixelSorter(object):
    def __init__(self, name, reverse=False):
        self.name = name
        self.reverse = reverse

    def to_string(self):
        return self.name

    def sort_pixels(self, pixels: list, img_width, img_height, criteria) -> list:
        pass


class BasicSorter(PixelSorter):
    def __init__(self, reverse=False):
        super().__init__("BasicSorter", reverse=reverse)

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        pixels.sort(key=criteria, reverse=self.reverse)
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__("Inverter")

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels
