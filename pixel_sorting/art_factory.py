import os

image_extensions = ["png", "jpg", ]


def apply_sorters_to_image(path_to_image):
    pass


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
