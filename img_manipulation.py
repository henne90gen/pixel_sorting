import math

from PIL import Image


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


# def sort(sort_mode, sort_criteria, img, x=0, y=0, width=0, height=0, radius=0, row=0, col=0):
#     pixels = get_pixels(img)
#     img_width = img.size[0]
#     img_height = img.size[1]
#
# if SortMode.All == sort_mode:
#     if sort_criteria is not None:
#         pixels.sort(key=sort_criteria.key)
# if SortMode.RectangleSort == sort_mode:
#     pixels = sort_rectangle(pixels, sort_criteria, img_width, img_height, x, y, width, height)
# if SortMode.CircleSort == sort_mode:
#     pixels = sort_circle(pixels, sort_criteria, img_width, img_height, x, y, radius)
# if SortMode.Invert == sort_mode:
#     pixels = invert(pixels)
# return pixels


def sort_rectangle(pixels, sort_criteria, img_width, img_height, x, y, width, height):
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

    sorting.sort(key=sort_criteria.key)

    index = 0
    for row in range(y, y + height):
        for col in range(x, x + width):
            pixels[row * img_width + col] = sorting[index]
            index += 1

    return pixels


def sort_circle(pixels, sort_criteria, img_width, img_height, x, y, radius):
    sorting = []
    for row in range(y - radius, y + radius):
        angle = 0
        if row < y:
            angle = math.asin((y - row) / radius)
        if row > y:
            angle = math.asin((row - y) / radius)
        for col in range(int(x - math.cos(angle) * radius), int(x + math.cos(angle) * radius)):
            sorting.append(pixels[row * img_width + col])

    sorting.sort(key=sort_criteria.key)

    index = 0
    for row in range(y - radius, y + radius):
        angle = 0
        if row < y:
            angle = math.asin((y - row) / radius)
        if row > y:
            angle = math.asin((row - y) / radius)
        for col in range(int(x - math.cos(angle) * radius), int(x + math.cos(angle) * radius)):
            pixels[row * img_width + col] = sorting[index]
            index += 1

    return pixels


def sort_row(pixels, sort_criteria, row, img_width, reverse=False):
    sorting = []
    for col in range(img_width):
        sorting.append(pixels[row * img_width + col])

    sorting.sort(key=sort_criteria.key, reverse=reverse)

    index = 0
    for col in range(img_width):
        pixels[row * img_width + col] = sorting[index]
        index += 1

    return pixels


def sort_column(pixels, sort_criteria, col, img_width, img_height, reverse=False):
    sorting = []
    for row in range(img_height):
        sorting.append(pixels[row * img_width + col])

    sorting.sort(key=sort_criteria.key, reverse=reverse)

    index = 0
    for row in range(img_height):
        pixels[row * img_width + col] = sorting[index]
        index += 1

    return pixels
