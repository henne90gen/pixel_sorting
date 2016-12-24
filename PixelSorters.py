from img_manipulation import *


class SortCriteria:
    def __init__(self, key):
        self.key = key


BuiltInSort = SortCriteria(lambda pixel: pixel)
RedSort = SortCriteria(lambda pixel: pixel[0])
GreenSort = SortCriteria(lambda pixel: pixel[1])
BlueSort = SortCriteria(lambda pixel: pixel[2])
BrightnessSort = SortCriteria(lambda pixel: pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114)
HueSort = SortCriteria(lambda pixel: pixel)  # TODO create more criteria


class PixelSorter(object):
    def __init__(self, img_width, img_height, sort_criteria):
        self.img_width = img_width
        self.img_height = img_height
        self.sort_criteria = sort_criteria

    def sort_pixels(self, pixels):
        pass

    def sort_image(self, img):
        return self.sort_pixels(get_pixels(img))


class AlternatingRowSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_height):
            pixels = sort_row(pixels, self.sort_criteria, i, self.img_width, reverse=reverse)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class AlternatingColumnSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_width):
            pixels = sort_column(pixels, self.sort_criteria, i, self.img_width, self.img_height, reverse=reverse)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__(0, 0, None)

    def sort_pixels(self, pixels):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels
