import os
from multiprocessing.dummy import Pool as ThreadPool

import time

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.pixel_sorters import *
from pixel_sorting.helper import *

all_sorters = [BasicSorter(), Inverter(), AlternatingRowSorter(), AlternatingRowSorter(alternation=10),
               AlternatingRowSorter(alternation=100), AlternatingColumnSorter(),
               AlternatingColumnSorter(alternation=10), AlternatingColumnSorter(alternation=100), DiamondSorter(),
               CircleSorter()]
max_index = len(all_sorters)
index = 0
for s in all_sorters:
    if type(s) == Inverter:
        continue
    all_sorters.append(CheckerBoardSorter(sorter=type(s)))
    index += 1
    if index >= max_index:
        break

favorite_sorters = [CheckerBoardSorter(sorter=AlternatingRowSorter), AlternatingRowSorter(),
                    AlternatingRowSorter(alternation=10), AlternatingColumnSorter(),
                    AlternatingColumnSorter(alternation=10)]


def get_generated_image_path(image_folder, sorter, criteria, extension):
    if isinstance(sorter, Inverter):
        return image_folder + sorter.to_string() + "." + extension
    return image_folder + sorter.to_string() + criteria + "." + extension


def apply_all_sorters_to_image(path_to_image):
    return apply_sorters_to_image([all_sorters, path_to_image])


def apply_favorite_sorters_to_image(path_to_image):
    return apply_sorters_to_image([favorite_sorters, path_to_image])


def apply_sorters_to_image(argument):
    """
    :param argument:
    0: array of sorter templates
    1: path to image
    """
    sorters = argument[0]
    path_to_image = argument[1]
    print("Started generating for " + path_to_image)

    image = Image.open(path_to_image)
    img_mode = image.mode
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
            image_path = get_generated_image_path(image_folder, sorter_template, criteria, extension)

            arguments.append([image_path, sorter_template, criteria, img_width, img_height, img_mode, img_pixels])
            if isinstance(sorter_template, Inverter):
                break

    result_list = thread_pool.map(apply_sorter_to_image, arguments)
    image.close()
    thread_pool.close()
    thread_pool.join()

    num_generated = 0
    for result in result_list:
        if result:
            num_generated += 1
    return num_generated


def apply_sorter_to_image(argument):
    """
    Uses a tuple of arguments, because thread_pool.map can only pass one argument
    :param argument:
    0: path to new image\n
    1: sorter template\n
    2: sort criteria\n
    3: width of image\n
    4: height of image\n
    5: mode of image\n
    6: pixels of image\n
    """
    sorter = argument[1].copy()
    sorter.img_width = argument[3]
    sorter.img_height = argument[4]
    sorter.criteria = sort_criteria.all_criteria[argument[2]]
    if os.path.isfile(argument[0]):
        return False
    temp_pixels = [p for p in argument[6]]
    sorter.sort_pixels(temp_pixels)
    save_to_img(argument[3], argument[4], argument[5], temp_pixels, argument[0])
    print("Generated", argument[0])
    return True


def apply_sorters_to_dir(path_to_dir, func_to_call):
    image_files = get_image_files(path_to_dir)
    print("Generating sorted images for:")
    for image in image_files:
        print(image)

    start_time = time.time()

    thread_pool = ThreadPool(processes=2)
    num_generated_list = thread_pool.map(func_to_call, image_files)
    thread_pool.close()
    thread_pool.join()

    stop_time = time.time()
    time_diff = stop_time - start_time

    total_generated = sum(num_generated_list)
    print()
    print("Done. Generated " + str(total_generated) + " sorted images in " + str(time_diff))
    print()
    return total_generated


def apply_all_sorters_to_dir(path_to_image):
    return apply_sorters_to_dir(path_to_image, apply_all_sorters_to_image)


def apply_favorite_sorters_to_dir(path_to_image):
    return apply_sorters_to_dir(path_to_image, apply_favorite_sorters_to_image)
