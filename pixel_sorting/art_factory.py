import logging
import multiprocessing
import os
import time
from multiprocessing import Process, Pipe
from queue import Queue
from typing import List

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_images, Timer, SortingImage, PixelImage
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


def run_sorters_on_directory(path_to_dir):
    images = get_images(path_to_dir)

    log.info("Generating sorted images for:")
    for image in images:
        log.info("\t" + str(image))

    sorters_to_use = get_all_sorters()
    # sorters_to_use = favorite_sorters
    # sorters_to_use = [AlternatingRowSorter(), AlternatingRowSorter(alternation=10),
    #                   AlternatingRowSorter(alternation=100)]
    # sorters_to_use = [CircleSorter()]
    # sorters_to_use = [CheckerBoardSorter(sorter=CircleSorter())]

    batches = create_batch_queue(images, sorters_to_use)

    with Timer(log, "Sorting Images"):
        num_processes = 8
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

                    parent_pipe, worker_pipe = Pipe()

                    process = Process(target=process_batch, args=(batch, worker_pipe))
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
