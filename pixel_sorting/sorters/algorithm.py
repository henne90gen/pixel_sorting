from pixel_sorting import sort_criteria

from pixel_sorting.sorters.basic import PixelSorter


class Algorithm(PixelSorter):
    def __init__(self):
        super().__init__("Algorithm")

    def sort_pixels(self, pixels: list, img_width: int, img_height: int, criteria=sort_criteria.built_in()) -> list:
        pass


class EdgeHighlighter(PixelSorter):
    def __init__(self):
        super().__init__("Algorithm")

    def sort_pixels(self, pixels: list, img_width: int, img_height: int, criteria=sort_criteria.built_in()) -> list:
        pass
