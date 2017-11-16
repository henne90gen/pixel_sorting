import logging
import os
import time
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from queue import Queue
from typing import List

from PIL import Image

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_image_files, get_pixels, remove_extension, save_to_img, get_images, get_extension, \
    Timer, SortingImage, PixelImage
from pixel_sorting.sorters.basic import PixelSorter, BasicSorter, Inverter
from pixel_sorting.sorters.checker_board import CheckerBoardSorter
from pixel_sorting.sorters.circle import CircleSorter
from pixel_sorting.sorters.column import AlternatingColumnSorter
from pixel_sorting.sorters.diamond import DiamondSorter
from pixel_sorting.sorters.row import AlternatingRowSorter

log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s"))
log.addHandler(handler)
log.setLevel(logging.INFO)

favorite_sorters = [CheckerBoardSorter(sorter=AlternatingRowSorter), AlternatingRowSorter(),
                    AlternatingRowSorter(alternation=10), AlternatingColumnSorter(),
                    AlternatingColumnSorter(alternation=10)]


def get_all_sorters() -> List[PixelSorter]:
    all_sorters = []
    all_sorters.extend([BasicSorter(), Inverter(), AlternatingRowSorter(), AlternatingRowSorter(alternation=10),
                        AlternatingRowSorter(alternation=100), AlternatingColumnSorter(),
                        AlternatingColumnSorter(alternation=10), AlternatingColumnSorter(alternation=100),
                        DiamondSorter(), CircleSorter()])

    max_index = len(all_sorters)
    index = 0
    for s in all_sorters:
        if type(s) == Inverter:
            continue
        all_sorters.append(CheckerBoardSorter(sorter=type(s)))
        index += 1
        if index >= max_index:
            break

    return all_sorters


def get_generated_image_path(image_folder, sorter, criteria, extension):
    if isinstance(sorter, Inverter):
        return image_folder + sorter.to_string() + "." + extension
    return image_folder + sorter.to_string() + criteria + "." + extension


def run_sorters_on_directory(path_to_dir):
    images = get_images(path_to_dir)

    log.info("Generating sorted images for:")
    for image in images:
        log.info("\t" + str(image))

    sorters_to_use = get_all_sorters()[:1]

    batches = create_batch_queue(images, sorters_to_use)

    with Timer(log, "Sorting Images"):
        num_processes = 8
        jobs = []
        try:
            while (not batches.empty()) or len(jobs) > 0:
                jobs = list(filter(lambda j: j.is_alive(), jobs))
                if len(jobs) < num_processes and not batches.empty():
                    batch = batches.get()
                    process = Process(target=process_batch, args=(batch,))
                    process.start()
                    jobs.append(process)
                    log.info(str(batches.qsize()) + " batches left")
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            # TODO print statistics
            pass


def create_batch_queue(images: List[PixelImage], sorters_to_use: List[PixelSorter], max_batch_size: int = 10) -> Queue:
    sorting_images = []
    for image in images:
        for sorter in sorters_to_use:
            for criteria in sort_criteria.all_criteria:
                sorting_images.append(SortingImage(image, sorter, criteria))

    batches = Queue()
    current_batch = []
    for image in sorting_images:
        current_batch.append(image)
        if len(current_batch) >= max_batch_size:
            batches.put(current_batch)
            current_batch = []
    return batches


def process_batch(batch: List[SortingImage], statistics: dict = None):
    # TODO gather statistics
    try:
        for img in batch:
            if os.path.isfile(img.get_new_path()):
                log.info("Skipping " + img.get_new_path())
                continue

            img.sort()
            img.save()

            log.info("Saved " + img.get_new_path())
    except KeyboardInterrupt:
        pass
