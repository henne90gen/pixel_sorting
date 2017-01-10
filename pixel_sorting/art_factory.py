import os
from multiprocessing.dummy import Pool as ThreadPool

import time

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.pixel_sorters import *
from pixel_sorting.helper import *

image_extensions = ["png", "jpg", "jpeg", ]
sorters = [BasicSorter(), Inverter(), AlternatingRowSorter(), AlternatingRowSorter(alternation=10),
           AlternatingRowSorter(alternation=100), AlternatingColumnSorter(), AlternatingColumnSorter(alternation=10),
           AlternatingColumnSorter(alternation=100), DiamondSorter(), CircleSorter(), CheckerBoardSorter()]


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


def apply_all_sorters_to_image(path_to_image):
    print(path_to_image)
    image = Image.open(path_to_image)
    img_width = image.size[0]
    img_height = image.size[1]
    img_pixels = get_pixels(image)
    extension = get_extension(path_to_image)

    image_folder = remove_extension(path_to_image) + "_generated/"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    thread_pool = ThreadPool(processes=12)

    arguments = []

    for sorter_template in sorters:
        for criteria in sort_criteria.all_criteria:
            image_path = generate_image_path(image_folder, sorter_template, criteria, extension)

            arguments.append([image, image_path, sorter_template, criteria, img_width, img_height, img_pixels])
            if isinstance(sorter_template, Inverter):
                break

    thread_pool.map(apply_sorter_to_image, arguments)
    image.close()
    thread_pool.close()
    thread_pool.join()


def apply_sorter_to_image(argument):
    sorter = argument[2].copy()
    sorter.img_width = argument[4]
    sorter.img_height = argument[5]
    sorter.criteria = sort_criteria.all_criteria[argument[3]]
    if os.path.isfile(argument[1]):
        return
    temp_pixels = [p for p in argument[6]]
    sorter.sort_pixels(temp_pixels)
    save_to_copy(argument[0], temp_pixels, argument[1])
    print("Generated", argument[1])


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


def get_image_files(path_to_dir):
    image_files = []
    for dir_name, sub_dir_names, file_names in os.walk(path_to_dir):
        for filename in file_names:
            if is_image_file(filename) and not is_generated_image(os.path.join(dir_name, filename)):
                image_files.append(os.path.join(dir_name, filename))
    return image_files


def apply_all_sorters_to_dir(path_to_dir):
    image_files = get_image_files(path_to_dir)
    print("Generating sorted images for:")

    start_time = time.time()

    thread_pool = ThreadPool(processes=2)
    thread_pool.map(apply_all_sorters_to_image, image_files)
    thread_pool.close()
    thread_pool.join()

    stop_time = time.time()

    time_diff = stop_time - start_time

    print("Done generating in " + str(time_diff))
