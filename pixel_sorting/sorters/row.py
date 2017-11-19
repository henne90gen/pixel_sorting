import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.sorters.basic import PixelSorter


class RowSorter(PixelSorter):
    def __init__(self, row, reverse=False):
        super().__init__("RowSorter", reverse)
        self.row = row

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        sorting = []
        for col in range(img_width):
            sorting.append(pixels[self.row * img_width + col])

        sorting.sort(key=criteria, reverse=self.reverse)

        index = 0
        for col in range(img_width):
            pixels[self.row * img_width + col] = sorting[index]
            index += 1
        return pixels


class AlternatingRowSorter(PixelSorter):
    def __init__(self, reverse=False, alternation=1):
        super().__init__("AlternatingRowSorter" + str(alternation), reverse)
        self.alternation = alternation

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        reverse = False
        for i in range(img_height):
            row_sorter = RowSorter(i, reverse)
            pixels = row_sorter.sort_pixels(pixels, img_width, img_height, criteria)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels
