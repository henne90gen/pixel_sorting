from pixel_sorting.art_factory import run_all_sorters_on_directory, run_sorters_on_directory
from pixel_sorting.sorters.basic import BasicSorter


def main():
    run_all_sorters_on_directory("./res")


if __name__ == "__main__":
    main()
