import sort_criteria
from sorters.basic import PixelSorter


class RowSorter(PixelSorter):
    def __init__(self, img_width, img_height, criteria, row, reverse=False):
        super().__init__("RowSorter", img_width, img_height, criteria, reverse)
        self.row = row

    def copy(self):
        return RowSorter(self.img_width, self.img_height, self.criteria, self.row, self.reverse)

    def sort_pixels(self, pixels):
        sorting = []
        for col in range(self.img_width):
            sorting.append(pixels[self.row * self.img_width + col])

        sorting.sort(key=self.criteria, reverse=self.reverse)

        index = 0
        for col in range(self.img_width):
            pixels[self.row * self.img_width + col] = sorting[index]
            index += 1
        return pixels


class AlternatingRowSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False, alternation=1):
        super().__init__("AlternatingRowSorter" + str(alternation), img_width, img_height, criteria, reverse)
        self.alternation = alternation

    def copy(self):
        return AlternatingRowSorter(self.img_width, self.img_height, self.criteria, self.reverse, self.alternation)

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_height):
            row_sorter = RowSorter(self.img_width, self.img_height, self.criteria, i, reverse)
            row_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels
