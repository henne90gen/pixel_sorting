import logging
import multiprocessing
import os
import time
from queue import Queue
from typing import List

import math
from PIL import Image

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_images, Timer, SortingImage, PixelImage, is_image_file
from pixel_sorting.sorters.basic import PixelSorter, BasicSorter, Inverter
from pixel_sorting.sorters.checker_board import CheckerBoardSorter
from pixel_sorting.sorters.circle import CircleSorter
from pixel_sorting.sorters.column import AlternatingColumnSorter
from pixel_sorting.sorters.diamond import DiamondSorter
from pixel_sorting.sorters.row import AlternatingRowSorter
from stencils import RectangleStencil

log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s"))
log.addHandler(handler)
log.setLevel(logging.INFO)

favorite_sorters = [CheckerBoardSorter(sorter=AlternatingRowSorter()), AlternatingRowSorter(),
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
        all_sorters.append(CheckerBoardSorter(sorter=s))
        index += 1
        if index >= max_index:
            break

    return all_sorters


def run_all_sorters_on_directory(path_to_dir: str):
    run_sorters_on_directory(path_to_dir, get_all_sorters())


def run_favorite_sorters_on_directory(path_to_dir: str):
    run_sorters_on_directory(path_to_dir, favorite_sorters)


def run_sorters_on_directory(path_to_dir: str, sorters_to_use):
    images = get_images(path_to_dir)

    log.info("Generating sorted images for:")
    for image in images:
        log.info("\t" + str(image))

    batches = create_batch_queue(images, sorters_to_use)

    with Timer(log, "Sorting Images"):
        num_processes = multiprocessing.cpu_count()
        jobs = []
        statistics = {"skipped": 0, "processed": 0, "errors": 0}
        try:
            while (not batches.empty()) or len(jobs) > 0:
                for _, pipe in jobs:
                    if pipe.poll():
                        try:
                            recv_stats = pipe.recv()
                            for key in recv_stats:
                                statistics[key] += recv_stats[key]
                        except EOFError:
                            pass

                jobs = list(filter(lambda j: j[0].is_alive(), jobs))

                if len(jobs) < num_processes and not batches.empty():
                    batch = batches.get()

                    parent_pipe, worker_pipe = multiprocessing.Pipe()

                    process = multiprocessing.Process(target=process_batch, args=(batch, worker_pipe))
                    process.start()

                    jobs.append((process, parent_pipe))

                    log.info(str(batches.qsize()) + " batches left")
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            total = statistics["processed"] + statistics["skipped"] + statistics["errors"]
            msg = "Finished {} total: {} processed, {} skipped, {} errors"
            log.info(msg.format(total, statistics["processed"], statistics["skipped"], statistics["errors"]))


def process_batch(batch: List[SortingImage], pipe):
    try:
        skipped = 0
        processed = 0
        errors = 0
        for img in batch:
            if os.path.isfile(img.get_new_path()):
                skipped += 1
                log.info("Skipping " + img.get_new_path())
                continue

            try:
                img.sort()
                img.save()

                processed += 1

                log.info("Saved " + img.get_new_path())
            except Exception as e:
                errors += 1
                log.info("Error processing " + img.get_new_path())
                log.debug(e)

        pipe.send({"skipped": skipped, "processed": processed, "errors": errors})
    except KeyboardInterrupt:
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


# def combine_images(path_to_dir: str):
#     image_files = list(map(lambda x: os.path.join(path_to_dir, x),
#                            filter(lambda x: is_image_file(x),
#                                   os.listdir(path_to_dir))))
#     mode = None
#     images = []
#     for path in image_files:
#         log.info(path)
#         image = Image.open(path)
#         mode = image.mode
#         width = image.size[0]
#         height = image.size[1]
#         images.append(PixelImage(width, height, [], path, mode))
#
#     dimension = int(math.sqrt(len(images))) + 1
#     width = dimension * images[0].width
#     height = dimension * images[0].height
#
#     with Timer(log, "Allocating memory"):
#         pixels = [0 for _ in range(width * height)]
#
#     with Timer(log, "Processing images"):
#         x = 0
#         y = 0
#         for index, image in enumerate(images):
#             log.info(str(len(images) - index) + " - " + str(image))
#
#             stencil = RectangleStencil(width, height, x, y, image.width, image.height)
#             image_pixels = image.load_pixels()
#             pixels = stencil.put_in_pixels(pixels, image_pixels)
#
#             x += image.width
#             if x >= width:
#                 y += image.height
#                 x = 0
#
#             del image_pixels
#             del image
#
#     new_image = Image.new(mode, (width, height))
#     new_image.putdata(pixels)
#     new_image.save(os.path.join(path_to_dir, 'overview.jpg'))
#     new_image.close()
