import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.sorters.basic import BasicSorter, PixelSorter
from pixel_sorting.stencils import RectangleStencil


class CheckerBoardSorter(PixelSorter):
    def __init__(self, reverse=False, sorter=BasicSorter(), width=8, height=8):
        super().__init__("CheckerBoardSorter" + str(width) + "x" + str(height) + "(" + sorter.to_string() + ")",
                         reverse)
        self.width = width
        self.height = height
        self.sorter = sorter

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        for x in range(self.width):
            for y in range(self.height):
                rect_width = round(img_width / self.width)
                rect_height = round(img_height / self.height)
                real_x = round(x * rect_width)
                real_y = round(y * rect_height)

                # FIXME Find a case where this path is walked!
                # if real_x >= img_width or real_y >= img_height:
                #     continue

                rect = RectangleStencil(img_width, img_height, real_x, real_y, rect_width, rect_height)
                rect_pixels = rect.cut_out_pixels(pixels)

                rect_pixels = self.sorter.sort_pixels(rect_pixels, rect_width, rect_height, criteria)
                pixels = rect.put_in_pixels(pixels, rect_pixels)
        return pixels


class ExtendedCheckerBoardSorter(PixelSorter):
    def __init__(self, reverse=False, criterias=None, sorters=None, width=8, height=8):
        super().__init__("ExtendedCheckerBoardSorter", reverse=reverse)
        if sorters is None:
            sorters = [BasicSorter for _ in range(width * height)]
        if criterias is None:
            criterias = [sort_criteria.built_in() for _ in range(width * height)]
        self.width = width
        self.height = height
        self.sorters = sorters
        self.criterias = criterias

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        sorter_index = 0
        criteria_index = 0

        for x in range(self.width):
            for y in range(self.height):

                if sorter_index >= len(self.sorters):
                    sorter_index = 0
                if criteria_index >= len(self.criterias):
                    criteria_index = 0

                rect_width = round(img_width / self.width)
                rect_height = round(img_height / self.height)
                real_x = round(x * rect_width)
                real_y = round(y * rect_height)
                rect = RectangleStencil(img_width, img_height, real_x, real_y, rect_width, rect_height)
                rect_pixels = rect.cut_out_pixels(pixels)

                sorter = self.sorters[sorter_index]()
                sorter.img_width = rect_width
                sorter.img_height = rect_height
                sorter.criteria = self.criterias[criteria_index]
                sorter.reverse = self.reverse

                rect_pixels = sorter.sort_pixels(rect_pixels, img_width, img_height, criteria)
                pixels = rect.put_in_pixels(pixels, rect_pixels)

                sorter_index += 1
                criteria_index += 1
        return pixels
