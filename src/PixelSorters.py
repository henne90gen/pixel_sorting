from src.helper import *


class SortCriteria:
    def __init__(self, key):
        self.key = key


BuiltInSort = SortCriteria(lambda pixel: pixel)
RedSort = SortCriteria(lambda pixel: pixel[0])
GreenSort = SortCriteria(lambda pixel: pixel[1])
BlueSort = SortCriteria(lambda pixel: pixel[2])
BrightnessSort = SortCriteria(lambda pixel: pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114)
AvgSort = SortCriteria(lambda pixel: (pixel[0] + pixel[1] + pixel[2]) / 3)
# TODO create more criteria


class PixelSorter(object):
    def __init__(self, img_width=0, img_height=0, sort_criteria=BuiltInSort):
        self.img_width = img_width
        self.img_height = img_height
        self.sort_criteria = sort_criteria

    def sort_pixels(self, pixels):
        pass

    def sort_image(self, img):
        return self.sort_pixels(get_pixels(img))


class BasicSorter(PixelSorter):
    def __init__(self, sort_criteria):
        super().__init__(sort_criteria=sort_criteria)

    def sort_pixels(self, pixels):
        pixels.sort(key=self.sort_criteria.key)
        return pixels


class RowSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, row, reverse=False):
        super().__init__(img_width, img_height, sort_criteria)
        self.row = row
        self.reverse = reverse

    def sort_pixels(self, pixels):
        sorting = []
        for col in range(self.img_width):
            sorting.append(pixels[self.row * self.img_width + col])

        sorting.sort(key=self.sort_criteria.key, reverse=self.reverse)

        index = 0
        for col in range(self.img_width):
            pixels[self.row * self.img_width + col] = sorting[index]
            index += 1
        return pixels


class AlternatingRowSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_height):
            row_sorter = RowSorter(self.img_width, self.img_height, self.sort_criteria, i, reverse)
            row_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class ColumnSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, column, reverse=False):
        super().__init__(img_width, img_height, sort_criteria)
        self.column = column
        self.reverse = reverse

    def sort_pixels(self, pixels):
        sorting = []
        for row in range(self.img_height):
            sorting.append(pixels[row * self.img_width + self.column])

        sorting.sort(key=self.sort_criteria.key, reverse=self.reverse)

        index = 0
        for row in range(self.img_height):
            pixels[row * self.img_width + self.column] = sorting[index]
            index += 1
        return pixels


class AlternatingColumnSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_width):
            column_sorter = ColumnSorter(self.img_width, self.img_height, self.sort_criteria, i, reverse)
            pixels = column_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__()

    def sort_pixels(self, pixels):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels
