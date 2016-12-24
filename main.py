from PixelSorters import *


def main():
    filename = "team-fortress.jpg"
    img = Image.open(filename)
    row_sorter = AlternatingRowSorter(img.size[0], img.size[1], BrightnessSort, 50)
    col_sorter = AlternatingColumnSorter(img.size[0], img.size[1], BrightnessSort, 1)
    pixels = row_sorter.sort_image(img)
    pixels = col_sorter.sort_pixels(pixels)
    pixels = Inverter().sort_pixels(pixels)
    save_to_copy(img, pixels, "copy_" + filename)


if __name__ == "__main__":
    main()
