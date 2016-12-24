from img_manipulation import *


def main():
    filename = "tree.jpg"
    img = Image.open(filename)
    pixels = sort(SortModes.CircleSort, img, x=50, y=50, radius=10)
    save_to_copy(img, pixels, "copy_" + filename)


if __name__ == "__main__":
    main()
