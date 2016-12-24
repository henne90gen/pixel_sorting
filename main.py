from img_manipulation import *


def main():
    filename = "pain.png"
    img = Image.open(filename)
    pixels = sort(SortModes.RectangleSort, img, 60, 100, 100, 100)
    save_to_copy(img, pixels, "copy_" + filename)


if __name__ == "__main__":
    main()
