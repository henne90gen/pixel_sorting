from PIL import Image


class SortModes:
    BuiltInSort = 0
    RedSort = 1
    GreenSort = 2
    BlueSort = 3
    BrightnessSort = 4
    RectangleSort = 5


def pixels_to_linear_array(pixels, width, height):
    result = []
    for y in range(height):
        for x in range(width):
            result.append(pixels[x, y])
    return result


def get_pixels(img):
    pixels = img.load()
    width = img.size[0]
    height = img.size[1]
    return pixels_to_linear_array(pixels, width, height)


def save_to_copy(img, pixels, filename):
    width = img.size[0]
    height = img.size[1]
    new_image = Image.new(img.mode, (width, height))
    new_image.putdata(pixels)
    new_image.save(filename)


def sort(sort_mode, img, x=0, y=0, width=0, height=0):
    pixels = get_pixels(img)
    img_width = img.size[0]
    img_height = img.size[1]
    if SortModes.BuiltInSort == sort_mode:
        pixels.sort()
    if SortModes.RedSort == sort_mode:
        pixels.sort(key=lambda pixel: pixel[0])
    if SortModes.GreenSort == sort_mode:
        pixels.sort(key=lambda pixel: pixel[1])
    if SortModes.BlueSort == sort_mode:
        pixels.sort(key=lambda pixel: pixel[2])
    if SortModes.BrightnessSort == sort_mode:
        pixels = sort_by_brightness(pixels)
    if SortModes.RectangleSort == sort_mode:
        pixels = sort_rectangle(pixels, img_width, img_height, x, y, width, height)
    return pixels


def sort_by_brightness(pixels):
    brightness = []
    for pixel in pixels:
        b = pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114
        brightness.append((b, pixel))
    brightness.sort(key=lambda tup: tup[0])
    pixels = [pixel[1] for pixel in brightness]
    return pixels


def sort_rectangle(pixels, img_width, img_height, x, y, width, height):
    sorting = []

    if y > img_height or x > img_width:
        return pixels
    if y + height > img_height:
        height = img_height - y
    if x + width > img_width:
        width = img_width - x

    for row in range(y, y + height):
        for col in range(x, x + width):
            sorting.append(pixels[row * img_width + col])

    sorting.sort()

    index = 0
    for row in range(y, y + height):
        for col in range(x, x + width):
            pixels[row * img_width + col] = sorting[index]
            index += 1

    return pixels


def sort_circle(pixels, img_width, img_height, x, y, radius):
    # TODO implement this
    return pixels
