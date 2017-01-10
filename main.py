from PIL import Image

from pixel_sorting.art_factory import apply_all_sorters_to_dir
from pixel_sorting.helper import get_pixels, save_to_copy
from pixel_sorting.pixel_sorters import CircleSorter
from pixel_sorting.sort_criteria import *


def main():
    # filename = "clouds.jpg"
    # img = Image.open("res/" + filename)
    # img_width = img.size[0]
    # img_height = img.size[1]
    #
    # pixels = get_pixels(img)
    #
    # circle_sorter = CircleSorter(img_width, img_height, SortCriteria.lightness(), True)
    # circle_sorter.sort_pixels(pixels)
    #
    # save_to_copy(img, pixels, "res/copy_" + filename)

    apply_all_sorters_to_dir("./res")

if __name__ == "__main__":
    main()
