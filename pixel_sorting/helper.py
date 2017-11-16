import logging
from typing import List, Callable

import time
from PIL import Image
import os

from pixel_sorting import sort_criteria

from pixel_sorting.sorters.basic import PixelSorter

image_extensions = ["png", "jpg", "jpeg", ]


class PixelImage:
    def __init__(self, width: int, height: int, pixels: list, file_path: str, mode):
        self.width = width
        self.height = height
        self.file_path = file_path
        self.dir_path = remove_extension(self.file_path)
        self.pixels = pixels
        self.mode = mode

    def __str__(self):
        return "{} ({}x{})".format(self.file_path, self.width, self.height)

    def get_extension(self):
        parts = self.file_path.split(".")
        return parts[-1]

    def create_directory(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)


class SortingImage:
    def __init__(self, pixel_image: PixelImage, sorter: PixelSorter, criteria: Callable):
        self.pixel_image = pixel_image
        self.pixels = []
        self.sorter = sorter
        self.criteria = criteria

    def get_new_path(self):
        parts = self.pixel_image.file_path.split("/")
        parts[-1] = remove_extension(parts[-1])
        parts.append(get_sorter_name(type(self.sorter)) + str(self.criteria) + "." + self.pixel_image.get_extension())
        return "/".join(parts)

    def sort(self):
        self.pixels = [p for p in self.pixel_image.pixels]
        self.sorter.criteria = sort_criteria.all_criteria[self.criteria]
        self.pixels = self.sorter.sort_pixels(self.pixels)

    def save(self):
        new_image = Image.new(self.pixel_image.mode, (self.pixel_image.width, self.pixel_image.height))
        new_image.putdata(self.pixels)
        new_image.save(self.get_new_path())
        new_image.close()


class Timer:
    def __init__(self, logger: logging.Logger, name: str):
        self.logger = logger
        self.name = name
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time.time()
        self.logger.info("Starting task '{}'".format(self.name))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.logger.info("Task '{}' finished after {} seconds".format(self.name, self.end - self.start))


def get_extension(path):
    # FIXME remove this method once refactoring is done (use PixelImage.get_extension instead)
    parts = path.split(".")
    return parts[-1]


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


def remove_extension(path):
    parts = path.split(".")
    new_path = ""
    for i in range(len(parts) - 1):
        new_path = new_path + parts[i]
    if path[0] == '.':
        new_path = "." + new_path
    return new_path


def get_image_files(path_to_dir: str) -> List[str]:
    files = os.listdir(path_to_dir)
    return list(map(lambda x: os.path.join(path_to_dir, x), filter(lambda x: is_image_file(x), files)))


def get_images(path_to_dir: str) -> List[PixelImage]:
    return list(
        map(create_pixel_image,
            map(lambda x: os.path.join(path_to_dir, x),
                filter(lambda x: is_image_file(x),
                       os.listdir(path_to_dir)))))


def create_pixel_image(path: str) -> PixelImage:
    image = Image.open(path)
    mode = image.mode
    width = image.size[0]
    height = image.size[1]
    pixels = get_pixels(image)
    return PixelImage(width, height, pixels, path, mode)


def get_sorter_name(sorter):
    result = str(sorter)
    result = result.split(".")[-1]
    result = result[:-2]
    return result
