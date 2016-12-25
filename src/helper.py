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

