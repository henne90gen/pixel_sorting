from src.PixelSorters import *

from src.Stencils import *


def main():
    filename = "team-fortress.jpg"
    img = Image.open("res/" + filename)
    img_width = img.size[0]
    img_height = img.size[1]

    rect = RectangleStencil(img_width, img_height, 100, 50, 1000, 500)
    rect_pixels = rect.cut_out_image(img)
    col_sorter = AlternatingColumnSorter(rect.width, rect.height, BrightnessSort, 1)
    rect_pixels = col_sorter.sort_pixels(rect_pixels)
    inverter = Inverter()
    rect_pixels = inverter.sort_pixels(rect_pixels)

    circ = CircleStencil(rect.width, rect.height, rect.width/2, rect.height/2, 200)
    circ_pixels = circ.cut_out_pixels(rect_pixels)
    circ_pixels = inverter.sort_pixels(circ_pixels)
    rect_pixels = circ.put_in_pixels(rect_pixels, circ_pixels)

    pixels = rect.put_in_image(img, rect_pixels)

    save_to_copy(img, pixels, "res/copy_" + filename)


if __name__ == "__main__":
    main()
