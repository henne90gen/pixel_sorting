from pixel_sorting.sorters.basic import PixelSorter


class ColumnSorter(PixelSorter):
    def __init__(self, column, reverse=False):
        super().__init__("ColumnSorter", reverse)
        self.column = column

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        sorting = []
        for row in range(img_height):
            sorting.append(pixels[row * img_width + self.column])

        sorting.sort(key=criteria, reverse=self.reverse)

        index = 0
        for row in range(img_height):
            pixels[row * img_width + self.column] = sorting[index]
            index += 1
        return pixels


class AlternatingColumnSorter(PixelSorter):
    def __init__(self, reverse=False, alternation=1):
        super().__init__("AlternatingColumnSorter" + str(alternation), reverse)
        self.alternation = alternation

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        reverse = False
        for i in range(img_width):
            column_sorter = ColumnSorter(i, reverse)
            pixels = column_sorter.sort_pixels(pixels, img_width, img_height, criteria)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels
