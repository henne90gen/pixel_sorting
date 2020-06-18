from pixel_sorting.art_factory import run_all_sorters_on_directory, run_sorters_on_directory
from pixel_sorting.sorters.basic import BasicSorter


def main():
    # run_all_sorters_on_directory("./res")
    # combine_images('./res/Snapchat-494567457')
    sorters = [BasicSorter()
#    CheckerBoardSorter(sorter=AlternatingRowSorter()), AlternatingRowSorter(),
#                AlternatingRowSorter(alternation=10), AlternatingColumnSorter(),
#                AlternatingColumnSorter(alternation=10)
                ]
    run_sorters_on_directory("./res", sorters)


if __name__ == "__main__":
    main()
