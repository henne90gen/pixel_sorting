from PIL import Image

from pixel_sorting.art_factory import apply_sorters_to_dir


def main():
    # filename = "planetside.jpg"
    # img = Image.open("res/" + filename)
    # img_width = img.size[0]
    # img_height = img.size[1]

    # pixels = get_pixels(img)

    # circle_sorter = CircleSorter(img_width, img_height, SortCriteria.lightness(), True)
    # circle_sorter.sort_pixels(pixels)

    # save_to_copy(img, pixels, "res/copy_" + filename)

    # apply_sorters_to_dir("./res")
    img = Image.open("res/city.jpg")
    print(img.mode)

if __name__ == "__main__":
    main()
