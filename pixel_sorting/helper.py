from PIL import Image
import os

image_extensions = ["png", "jpg", "jpeg", ]


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
    new_image.close()


def is_image_file(filename):
    parts = filename.split('.')
    for part in parts:
        if part.lower() in image_extensions:
            return True
    return False


def is_generated_image(path):
    parts = path.split("/")
    if "generated" in parts[len(parts) - 2]:
        return True
    return False


def get_extension(path):
    parts = path.split(".")
    return parts[-1]


def remove_extension(path):
    parts = path.split(".")
    new_path = ""
    for i in range(len(parts) - 1):
        new_path = new_path + parts[i]
    if path[0] == '.':
        new_path = "." + new_path
    return new_path


def get_image_files(path_to_dir):
    image_files = os.listdir(path_to_dir)
    return list(map(lambda x: os.path.join(path_to_dir, x), filter(lambda x: is_image_file(x), image_files)))


def get_sorter_name(sorter):
    result = str(sorter)
    result = result.split(".")[-1]
    result = result[:-2]
    return result
