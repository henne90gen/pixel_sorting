import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.sorters.basic import PixelSorter


class ColumnSorter(PixelSorter):
    def __init__(self, img_width, img_height, criteria, column, reverse=False):
        super().__init__("ColumnSorter", img_width, img_height, criteria, reverse)
        self.column = column

    def copy(self):
        return ColumnSorter(self.img_width, self.img_height, self.criteria, self.column, self.reverse)

    def sort_pixels(self, pixels):
        sorting = []
        for row in range(self.img_height):
            sorting.append(pixels[row * self.img_width + self.column])

        sorting.sort(key=self.criteria, reverse=self.reverse)

        index = 0
        for row in range(self.img_height):
            pixels[row * self.img_width + self.column] = sorting[index]
            index += 1
        return pixels


class AlternatingColumnSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False, alternation=1):
        super().__init__("AlternatingColumnSorter" + str(alternation), img_width, img_height, criteria, reverse)
        self.alternation = alternation

    def copy(self):
        return AlternatingColumnSorter(self.img_width, self.img_height, self.criteria, self.reverse, self.alternation)

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_width):
            column_sorter = ColumnSorter(self.img_width, self.img_height, self.criteria, i, reverse)
            pixels = column_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels
