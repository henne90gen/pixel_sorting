import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_pixels, get_sorter_name
from pixel_sorting.stencils import RectangleStencil


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


class CheckerBoardSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False,
                 sorter=BasicSorter, width=8, height=8):
        super().__init__("CheckerBoardSorter" + get_sorter_name(sorter), img_width, img_height, criteria, reverse)
        self.width = width
        self.height = height
        self.sorter = sorter

    def copy(self):
        return CheckerBoardSorter(self.img_width, self.img_height, self.criteria, self.reverse, self.sorter, self.width,
                                  self.height)

    def sort_pixels(self, pixels):
        for x in range(self.width):
            for y in range(self.height):
                rect_width = round(self.img_width / self.width)
                rect_height = round(self.img_height / self.height)
                real_x = round(x * rect_width)
                real_y = round(y * rect_height)
                if real_x >= self.img_width or real_y >= self.img_height:
                    continue
                rect = RectangleStencil(self.img_width, self.img_height, real_x, real_y, rect_width, rect_height)
                rect_pixels = rect.cut_out_pixels(pixels)

                sorter = self.sorter()
                sorter.img_width = rect_width
                sorter.img_height = rect_height
                sorter.criteria = self.criteria
                sorter.reverse = self.reverse

                rect_pixels = sorter.sort_pixels(pixels=rect_pixels)
                pixels = rect.put_in_pixels(pixels, rect_pixels)
        return pixels


class ExtendedCheckerBoardSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criterias=None, reverse=False,
                 sorters=None, width=8, height=8):
        super().__init__("ExtendedCheckerBoardSorter", img_width, img_height, reverse=reverse)
        if sorters is None:
            sorters = [BasicSorter for _ in range(8 * 8)]
        if criterias is None:
            criterias = [sort_criteria.built_in() for _ in range(8 * 8)]
        self.width = width
        self.height = height
        self.sorters = sorters
        self.criterias = criterias

    def copy(self):
        return ExtendedCheckerBoardSorter(self.img_width, self.img_height, self.criteria, self.reverse, self.sorters,
                                          self.width, self.height)

    def sort_pixels(self, pixels):
        sorter_index = 0
        criteria_index = 0

        for x in range(self.width):
            for y in range(self.height):

                if sorter_index >= len(self.sorters):
                    sorter_index = 0
                if criteria_index >= len(self.criterias):
                    criteria_index = 0

                rect_width = round(self.img_width / self.width)
                rect_height = round(self.img_height / self.height)
                real_x = round(x * rect_width)
                real_y = round(y * rect_height)
                rect = RectangleStencil(self.img_width, self.img_height, real_x, real_y, rect_width, rect_height)
                rect_pixels = rect.cut_out_pixels(pixels)

                sorter = self.sorters[sorter_index]()
                sorter.img_width = rect_width
                sorter.img_height = rect_height
                sorter.criteria = self.criterias[criteria_index]
                sorter.reverse = self.reverse

                rect_pixels = sorter.sort_pixels(pixels=rect_pixels)
                pixels = rect.put_in_pixels(pixels, rect_pixels)

                sorter_index += 1
                criteria_index += 1
        return pixels
