def main():
    filename = "team-fortress.jpg"
    img = Image.open("res/" + filename)
    img_width = img.size[0]
    img_height = img.size[1]

    pixels = get_pixels(img)

    circle_sorter = CircleSorter(img_width, img_height, SortCriteria.brightness())
    circle_sorter.sort_pixels(pixels)

    save_to_copy(img, pixels, "res/copy_" + filename)


if __name__ == "__main__":
    print(math.pi / 4)
    print(math.cos(math.pi/4))
    angle = math.atan2(-0.5, -0.5)
    print(angle)
    # main()
