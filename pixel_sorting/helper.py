from PIL import Image


def pixels_to_linear_array(pixels, width, height):
    result = []
    for y in range(height):
        for x in range(width):
            result.append(pixels[x, y])
    return result


def get_pixels(image):
    pixels = image.load()
    width = image.size[0]
    height = image.size[1]
    return pixels_to_linear_array(pixels, width, height)


def save_to_copy(img, pixels, filename):
    width = img.size[0]
    height = img.size[1]
    save_to_img(width, height, img.mode, pixels, filename)


def save_to_img(width, height, mode, pixels, filename):
    new_image = Image.new(mode, (width, height))
    new_image.putdata(pixels)
    new_image.save(filename)
