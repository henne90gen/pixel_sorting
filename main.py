from pixel_sorting import *


def main():
    filename = "team-fortress.jpg"
    img = Image.open("res/" + filename)
    img_width = img.size[0]
    img_height = img.size[1]

    pixels = get_pixels(img)

    circle_sorter = DiamondSorter(img_width, img_height, SortCriteria.avg(), True)
    circle_sorter.sort_pixels(pixels)

    save_to_copy(img, pixels, "res/copy_" + filename)


if __name__ == "__main__":
    main()
