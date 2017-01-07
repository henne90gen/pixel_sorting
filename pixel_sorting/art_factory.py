import os
from multiprocessing.dummy import Pool as ThreadPool

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.pixel_sorters import *
from pixel_sorting.helper import *

image_extensions = ["png", "jpg", "jpeg", ]
sorters = [BasicSorter(), Inverter(), AlternatingRowSorter(), AlternatingRowSorter(alternation=10),
           AlternatingRowSorter(alternation=100), AlternatingColumnSorter(), AlternatingColumnSorter(alternation=10),
           AlternatingColumnSorter(alternation=100), DiamondSorter(),
           CircleSorter()]


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


def generate_image_path(image_folder, sorter, criteria, extension):
    if isinstance(sorter, Inverter):
        return image_folder + sorter.to_string() + "." + extension
    return image_folder + sorter.to_string() + criteria + "." + extension


def apply_sorters_to_image(path_to_image):
    print(path_to_image)
    image = Image.open(path_to_image)
    img_width = image.size[0]
    img_height = image.size[1]
    img_pixels = get_pixels(image)
    extension = get_extension(path_to_image)

    image_folder = remove_extension(path_to_image) + "_folder/"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for sorter in sorters:
        for criteria in sort_criteria.all_criteria:
            sorter.img_width = img_width
            sorter.img_height = img_height
            sorter.sort_criteria = sort_criteria.all_criteria[criteria]

            temp_pixels = [p for p in img_pixels]
            sorter.sort_pixels(temp_pixels)
            new_path = generate_image_path(image_folder, sorter, criteria, extension)
            save_to_copy(image, temp_pixels, new_path)

            print("Generated", new_path)

            if isinstance(sorter, Inverter):
                break


def is_image_file(filename):
    parts = filename.split('.')
    for part in parts:
        if part.lower() in image_extensions:
            return True
    return False


def get_image_files(path_to_dir):
    image_files = []
    for dir_name, sub_dir_names, file_names in os.walk(path_to_dir):
        for filename in file_names:
            if is_image_file(filename):
                image_files.append(os.path.join(dir_name, filename))
    return image_files


def apply_sorters_to_dir(path_to_dir):
    image_files = get_image_files(path_to_dir)
    print("Generating sorted images for:")
    pool = ThreadPool(12)

    pool.map(apply_sorters_to_image, image_files)
    pool.close()
    pool.join()

    print("Done generating.")
