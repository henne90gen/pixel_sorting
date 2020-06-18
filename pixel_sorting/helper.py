import logging
import os
import time
from typing import List

import cv2
import numpy as np

from pixel_sorting import sort_criteria
from pixel_sorting.sorters.basic import PixelSorter

image_extensions = ["png", "jpg", "jpeg"]


class PixelImage:
    def __init__(self, width: int, height: int, file_path: str):
        self.width = width
        self.height = height
        self.file_path = file_path
        self.dir_path = remove_extension(self.file_path)
        self.pixels = None

    def __str__(self):
        return f"{self.file_path} ({self.width}x{self.height})"

    def __eq__(self, other):
        if not isinstance(other, PixelImage):
            return False
        return self.width == other.width and self.height == other.height and self.file_path == other.file_path

    def load_pixels(self) -> list:
        if self.pixels is None:
            self.pixels = cv2.imread(self.file_path)
        self.pixels = self.pixels.reshape((self.width * self.height, 3))
        return self.pixels

    def get_extension(self):
        parts = self.file_path.split(".")
        return parts[-1]

    def create_directory(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)


class SortingImage:
    def __init__(self, pixel_image: PixelImage, sorter: PixelSorter, criteria: str):
        self.pixel_image = pixel_image
        self.pixels = []
        self.sorter = sorter
        self.criteria = criteria

    def __str__(self):
        return "{}: {} {}".format(str(self.pixel_image), self.sorter, self.criteria)

    def __eq__(self, other):
        if not isinstance(other, SortingImage):
            return False
        return self.pixel_image == other.pixel_image and self.sorter.name == other.sorter.name and self.criteria == other.criteria

    def get_new_path(self):
        parts = self.pixel_image.file_path.split("/")
        parts[-1] = remove_extension(parts[-1])
        parts.append(str(self.sorter) + str(self.criteria) +
                     "." + self.pixel_image.get_extension())
        return "/".join(parts)

    def sort(self):
        self.pixels = [p for p in self.pixel_image.load_pixels()]
        criteria = sort_criteria.all_criteria[self.criteria]
        self.pixels = self.sorter.sort_pixels(
            self.pixels, self.pixel_image.height, self.pixel_image.width, criteria)

    def save(self):
        self.pixel_image.create_directory()
        cv2.imwrite(self.get_new_path(), np.array(self.pixels).reshape(
            (self.pixel_image.width, self.pixel_image.height, 3)))


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
        time_difference = self.end - self.start
        self.logger.info("Task '{}' finished after {:.3f}s".format(
            self.name, time_difference))


def get_pixels(image):
    pixels = image.load()
    width = image.size[0]
    height = image.size[1]
    result = []
    for y in range(height):
        for x in range(width):
            result.append(pixels[x, y])
    return result


def save_to_image(width, height, mode, pixels, filename):
    cv2.imwrite(filename, np.array(pixels))


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


def get_images(path_to_dir: str) -> List[PixelImage]:
    return list(
        map(create_pixel_image,
            map(lambda x: os.path.join(path_to_dir, x),
                filter(lambda x: is_image_file(x),
                       os.listdir(path_to_dir)))))


def create_pixel_image(path: str) -> PixelImage:
    pixels = cv2.imread(path)
    width = pixels.shape[0]
    height = pixels.shape[1]
    return PixelImage(width, height, path)
