from .test_helper import *
from pixel_sorting.pixel_sorters import *
from PIL import Image

test_image_path = "./pixel_sorting/tests/test_image_sorters.jpg"


class SorterTests(unittest.TestCase):
    def testPixelSorter(self):
        sorter = PixelSorter("")
        sorter_img = Image.open(test_image_path)
        sorter_pixels = []
        self.assertEqual(sorter.sort_image(sorter_img), None)
        self.assertEqual(sorter.sort_pixels(sorter_pixels), None)

    inverter_pixels = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    inverter_result = [(255, 255, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 0)]

    def testInverter(self):
        inverter = Inverter()
        test_pixels = [p for p in self.inverter_pixels]
        self.assertEqual(inverter.sort_pixels(test_pixels), self.inverter_result)
        self.assertEqual(test_pixels, self.inverter_result)

    basic_pixels = [(6, 3, 1), (7, 24, 3), (15, 11, 2), (12, 17, 5), (16, 27, 18), (23, 10, 15)]
    basic_builtin_result = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
    basic_red_result = [(6, 3, 1), (7, 24, 3), (12, 17, 5), (15, 11, 2), (16, 27, 18), (23, 10, 15)]
    basic_green_result = [(6, 3, 1), (23, 10, 15), (15, 11, 2), (12, 17, 5), (7, 24, 3), (16, 27, 18)]
    basic_blue_result = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]
    basic_brightness_result = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (23, 10, 15), (7, 24, 3), (16, 27, 18)]
    basic_avg_result = [(6, 3, 1), (15, 11, 2), (7, 24, 3), (12, 17, 5), (23, 10, 15), (16, 27, 18)]
    basic_hue = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (7, 24, 3), (16, 27, 18), (23, 10, 15)]
    basic_saturation = [(16, 27, 18), (23, 10, 15), (12, 17, 5), (6, 3, 1), (15, 11, 2), (7, 24, 3)]
    basic_lightness = [(6, 3, 1), (15, 11, 2), (12, 17, 5), (7, 24, 3), (23, 10, 15), (16, 27, 18)]

    def testBasicSorter(self):
        basic_sorter = BasicSorter(sort_criteria.built_in())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_builtin_result)

        basic_sorter = BasicSorter(sort_criteria.red())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_red_result)

        basic_sorter = BasicSorter(sort_criteria.green())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_green_result)

        basic_sorter = BasicSorter(sort_criteria.blue())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_blue_result)

        basic_sorter = BasicSorter(sort_criteria.brightness())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_brightness_result)

        basic_sorter = BasicSorter(sort_criteria.avg())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_avg_result)

        basic_sorter = BasicSorter(sort_criteria.hue())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_hue)

        basic_sorter = BasicSorter(sort_criteria.saturation())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_saturation)

        basic_sorter = BasicSorter(sort_criteria.lightness())
        execute_sorter(self, basic_sorter, self.basic_pixels, self.basic_lightness)

    row_pixels = [4, 2, 3, 5, 1,
                  3, 1, 5, 2, 4]
    row_result1 = [1, 2, 3, 4, 5,
                   3, 1, 5, 2, 4]
    row_result2 = [4, 2, 3, 5, 1,
                   5, 4, 3, 2, 1]

    def testRowSorter(self):
        row_sorter = RowSorter(5, 2, sort_criteria.built_in(), 0)
        execute_sorter(self, row_sorter, self.row_pixels, self.row_result1)

        row_sorter = RowSorter(5, 2, sort_criteria.built_in(), 1, True)
        execute_sorter(self, row_sorter, self.row_pixels, self.row_result2)

    alt_pixels = [p for p in range(1, 26)]
    alt_row_result = [1, 2, 3, 4, 5, 10, 9, 8, 7, 6, 11, 12, 13, 14, 15, 20, 19, 18, 17, 16, 21, 22, 23, 24, 25]

    def testAlternatingRowSorter(self):
        row_sorter = AlternatingRowSorter(5, 5, sort_criteria.built_in(), 1)
        execute_sorter(self, row_sorter, self.alt_pixels, self.alt_row_result)

    col_pixels = [4, 7, 3, 9, 1, 6, 5, 8, 2, 10]
    col_result1 = [1, 7, 2, 9, 3, 6, 4, 8, 5, 10]
    col_result2 = [4, 10, 3, 9, 1, 8, 5, 7, 2, 6]

    def testColumnSorter(self):
        col_sorter = ColumnSorter(2, 5, sort_criteria.built_in(), 0, False)
        execute_sorter(self, col_sorter, self.col_pixels, self.col_result1)

        col_sorter.column = 1
        col_sorter.reverse = True
        execute_sorter(self, col_sorter, self.col_pixels, self.col_result2)

    alt_col_result = [1, 22, 3, 24, 5, 6, 17, 8, 19, 10, 11, 12, 13, 14, 15, 16, 7, 18, 9, 20, 21, 2, 23, 4, 25]

    def testAlternatingColumnSorter(self):
        col_sorter = AlternatingColumnSorter(5, 5, sort_criteria.built_in(), 1)
        execute_sorter(self, col_sorter, self.alt_pixels, self.alt_col_result)

    diamond_pixels = [p for p in range(1, 26)]
    diamond_result = [24, 19, 12, 20, 25,
                      18, 11, 5, 13, 21,
                      10, 4, 1, 2, 6,
                      17, 9, 3, 7, 14,
                      23, 16, 8, 15, 22]

    def testDiamondSorter(self):
        diamond_sorter = DiamondSorter(5, 5, sort_criteria.built_in(), False)

        self.assertEqual(diamond_sorter.next_position((0, 0)), (1, 0))
        self.assertEqual(diamond_sorter.next_position((1, 0)), (0, 1))
        self.assertEqual(diamond_sorter.next_position((0, 1)), (-1, 0))
        self.assertEqual(diamond_sorter.next_position((-1, 0)), (0, -1))
        self.assertEqual(diamond_sorter.next_position((0, -1)), (2, 0))

        self.assertEqual(diamond_sorter.next_position((2, 0)), (1, 1))
        self.assertEqual(diamond_sorter.next_position((1, 1)), (0, 2))
        self.assertEqual(diamond_sorter.next_position((0, 2)), (-1, 1))
        self.assertEqual(diamond_sorter.next_position((-1, 1)), (-2, 0))
        self.assertEqual(diamond_sorter.next_position((-2, 0)), (-1, -1))
        self.assertEqual(diamond_sorter.next_position((-1, -1)), (0, -2))
        self.assertEqual(diamond_sorter.next_position((0, -2)), (1, -1))
        self.assertEqual(diamond_sorter.next_position((1, -1)), (3, 0))

        self.assertEqual(diamond_sorter.next_position((3, 0)), (2, 1))
        self.assertEqual(diamond_sorter.next_position((2, 1)), (1, 2))
        self.assertEqual(diamond_sorter.next_position((1, 2)), (0, 3))
        self.assertEqual(diamond_sorter.next_position((0, 3)), (-1, 2))
        self.assertEqual(diamond_sorter.next_position((-1, 2)), (-2, 1))
        self.assertEqual(diamond_sorter.next_position((-2, 1)), (-3, 0))
        self.assertEqual(diamond_sorter.next_position((-3, 0)), (-2, -1))
        self.assertEqual(diamond_sorter.next_position((-2, -1)), (-1, -2))
        self.assertEqual(diamond_sorter.next_position((-1, -2)), (0, -3))
        self.assertEqual(diamond_sorter.next_position((0, -3)), (1, -2))
        self.assertEqual(diamond_sorter.next_position((1, -2)), (2, -1))
        self.assertEqual(diamond_sorter.next_position((2, -1)), (4, 0))

        self.assertEqual(diamond_sorter.next_position((4, 0)), (3, 1))
        self.assertEqual(diamond_sorter.next_position((3, 1)), (2, 2))
        self.assertEqual(diamond_sorter.next_position((2, 2)), (1, 3))
        self.assertEqual(diamond_sorter.next_position((1, 3)), (0, 4))
        self.assertEqual(diamond_sorter.next_position((0, 4)), (-1, 3))
        self.assertEqual(diamond_sorter.next_position((-1, 3)), (-2, 2))
        self.assertEqual(diamond_sorter.next_position((-2, 2)), (-3, 1))
        self.assertEqual(diamond_sorter.next_position((-3, 1)), (-4, 0))
        self.assertEqual(diamond_sorter.next_position((-4, 0)), (-3, -1))
        self.assertEqual(diamond_sorter.next_position((-3, -1)), (-2, -2))
        self.assertEqual(diamond_sorter.next_position((-2, -2)), (-1, -3))
        self.assertEqual(diamond_sorter.next_position((-1, -3)), (0, -4))
        self.assertEqual(diamond_sorter.next_position((0, -4)), (1, -3))
        self.assertEqual(diamond_sorter.next_position((1, -3)), (2, -2))
        self.assertEqual(diamond_sorter.next_position((2, -2)), (3, -1))
        self.assertEqual(diamond_sorter.next_position((3, -1)), (5, 0))

        execute_sorter(self, diamond_sorter, self.diamond_pixels, self.diamond_result)

    pixel_source = [p for p in range(50, 99)]
    circle_pixels = [p for p in range(1, 26)]
    circle_pixel_result = [1, 2, 3, 4, 5,
                           6, 7, 8, 9, 10,
                           11, 12, 13, 50, 15,
                           16, 17, 18, 19, 20,
                           21, 22, 23, 24, 25]
    circle_octant_result1 = [1, 2, 3, 4, 5,
                             6, 7, 53, 9, 10,
                             11, 51, 13, 50, 15,
                             16, 17, 52, 19, 20,
                             21, 22, 23, 24, 25]
    circle_octant_result2 = [1, 2, 3, 4, 5,
                             6, 52, 8, 53, 10,
                             11, 12, 13, 14, 15,
                             16, 51, 18, 50, 20,
                             21, 22, 23, 24, 25]
    circle_octant_result3 = [1, 57, 3, 55, 5,
                             52, 7, 8, 9, 53,
                             11, 12, 13, 14, 15,
                             51, 17, 18, 19, 50,
                             21, 56, 23, 54, 25]
    circle_radius_result1 = [1, 2, 3, 4, 5,
                             6, 7, 53, 9, 10,
                             11, 51, 13, 50, 15,
                             16, 17, 52, 19, 20,
                             21, 22, 23, 24, 25]
    circle_radius_result2 = [1, 2, 3, 4, 5,
                             6, 56, 53, 57, 10,
                             11, 51, 13, 50, 15,
                             16, 55, 52, 54, 20,
                             21, 22, 23, 24, 25]
    circle_radius_result3 = [1, 61, 53, 59, 5,
                             56, 7, 8, 9, 57,
                             51, 12, 13, 14, 50,
                             55, 17, 18, 19, 54,
                             21, 60, 52, 58, 25]
    circle_radius_result4 = [1, 61, 53, 59, 5,
                             56, 7, 8, 9, 57,
                             51, 12, 13, 14, 50,
                             55, 17, 18, 19, 54,
                             21, 60, 52, 58, 25]
    circle_radius_result5 = [52, 2, 3, 4, 53,
                             6, 7, 8, 9, 10,
                             11, 12, 13, 14, 15,
                             16, 17, 18, 19, 20,
                             51, 22, 23, 24, 50]
    circle_result = [24, 21, 13, 19, 25,
                     16, 8, 5, 9, 17,
                     11, 3, 1, 2, 10,
                     15, 7, 4, 6, 14,
                     23, 20, 12, 18, 22]

    def testCircleSorter(self):
        circle_sorter = CircleSorter(5, 5, sort_criteria.built_in())

        execute_draw_pixel(self, circle_sorter, 1, 0, 0, self.circle_pixel_result, 1)
        execute_draw_pixel(self, circle_sorter, 3, 0, 0, self.circle_pixels, 0)
        execute_draw_pixel(self, circle_sorter, -3, 0, 0, self.circle_pixels, 0)
        execute_draw_pixel(self, circle_sorter, 0, -3, 0, self.circle_pixels, 0)
        execute_draw_pixel(self, circle_sorter, -3, -3, 0, self.circle_pixels, 0)
        execute_draw_pixel(self, circle_sorter, 0, 0, len(self.pixel_source), self.circle_pixels, 0)

        execute_draw_octants(self, circle_sorter, 1, 0, self.circle_octant_result1, 4)
        execute_draw_octants(self, circle_sorter, 1, 1, self.circle_octant_result2, 4)
        execute_draw_octants(self, circle_sorter, 2, 1, self.circle_octant_result3, 8)

        execute_draw_circle(self, circle_sorter, self.circle_radius_result1, 1)
        execute_draw_circle(self, circle_sorter, self.circle_radius_result2, 1.5)

        execute_draw_circle(self, circle_sorter, self.circle_radius_result3, 2)
        execute_draw_circle(self, circle_sorter, self.circle_radius_result4, 2.5)
        execute_draw_circle(self, circle_sorter, self.circle_radius_result5, 3)

        execute_sorter(self, circle_sorter, self.circle_pixels, self.circle_result)
        for p in self.circle_pixels:
            self.assertTrue(p in self.circle_result)

    def testCircleSorterWithRealFile(self):
        img = Image.open(test_image_path)
        img_width = img.size[0]
        img_height = img.size[1]

        pixels = get_pixels(img)

        pixel_dict = {}
        for p in pixels:
            if p not in pixel_dict:
                pixel_dict[p] = 0
            pixel_dict[p] += 1

        new_pixels = [p for p in pixels]

        circle_sorter = CircleSorter(img_width, img_height, sort_criteria.built_in(), False)
        circle_sorter.sort_pixels(new_pixels)

        self.assertEqual(len(new_pixels), len(pixels), "The new image doesn't have the same number of pixels.")
        for p in new_pixels:
            self.assertTrue(p in pixels)

        new_pixel_dict = {}
        for p in pixels:
            if p not in new_pixel_dict:
                new_pixel_dict[p] = 0
            new_pixel_dict[p] += 1

        for p in new_pixel_dict:
            self.assertTrue(p in pixel_dict)
            self.assertEqual(new_pixel_dict[p], pixel_dict[p])

    board_square = [p for p in range(1, 16 * 16 + 1)[::-1]]
    board_square_result = [239, 240, 237, 238, 235, 236, 233, 234, 231, 232, 229, 230, 227, 228, 225, 226, 255, 256,
                           253, 254, 251, 252, 249, 250, 247, 248, 245, 246, 243, 244, 241, 242, 207, 208, 205, 206,
                           203, 204, 201, 202, 199, 200, 197, 198, 195, 196, 193, 194, 223, 224, 221, 222, 219, 220,
                           217, 218, 215, 216, 213, 214, 211, 212, 209, 210, 175, 176, 173, 174, 171, 172, 169, 170,
                           167, 168, 165, 166, 163, 164, 161, 162, 191, 192, 189, 190, 187, 188, 185, 186, 183, 184,
                           181, 182, 179, 180, 177, 178, 143, 144, 141, 142, 139, 140, 137, 138, 135, 136, 133, 134,
                           131, 132, 129, 130, 159, 160, 157, 158, 155, 156, 153, 154, 151, 152, 149, 150, 147, 148,
                           145, 146, 111, 112, 109, 110, 107, 108, 105, 106, 103, 104, 101, 102, 99, 100, 97, 98, 127,
                           128, 125, 126, 123, 124, 121, 122, 119, 120, 117, 118, 115, 116, 113, 114, 79, 80, 77, 78,
                           75, 76, 73, 74, 71, 72, 69, 70, 67, 68, 65, 66, 95, 96, 93, 94, 91, 92, 89, 90, 87, 88, 85,
                           86, 83, 84, 81, 82, 47, 48, 45, 46, 43, 44, 41, 42, 39, 40, 37, 38, 35, 36, 33, 34, 63, 64,
                           61, 62, 59, 60, 57, 58, 55, 56, 53, 54, 51, 52, 49, 50, 15, 16, 13, 14, 11, 12, 9, 10, 7, 8,
                           5, 6, 3, 4, 1, 2, 31, 32, 29, 30, 27, 28, 25, 26, 23, 24, 21, 22, 19, 20, 17, 18]
    board_rect = []

    def testCheckerBoardSorter(self):
        board_sorter = CheckerBoardSorter(16, 16)
        execute_sorter(self, board_sorter, self.board_square, self.board_square_result)

    def testExtendedCheckerBoardSorter(self):
        board_sorter = ExtendedCheckerBoardSorter(16, 16)
        execute_sorter(self, board_sorter, self.board_square, self.board_square_result)

    def testCopy(self):
        sorter = ColumnSorter(6, 5, sort_criteria.built_in(), 2)
        sort_copy = sorter.copy()
        self.assertEqual(sort_copy.criteria, sorter.criteria)
        self.assertEqual(sort_copy.name, sorter.name)
        self.assertEqual(sort_copy.img_width, 6)
        self.assertEqual(sort_copy.img_height, 5)
        self.assertEqual(sort_copy.column, 2)

        sorter = RowSorter(6, 5, sort_criteria.avg(), 3)
        sort_copy = sorter.copy()
        self.assertEqual(sort_copy.criteria, sorter.criteria)
        self.assertEqual(sort_copy.name, sorter.name)
        self.assertEqual(sort_copy.img_width, 6)
        self.assertEqual(sort_copy.img_height, 5)
        self.assertEqual(sort_copy.row, 3)

        PixelSorter("").copy()

        sorter = ExtendedCheckerBoardSorter(6, 5, sort_criteria.avg(), False, None, 3, 4)
        sort_copy = sorter.copy()
        self.assertEqual(sort_copy.criteria, sorter.criteria)
        self.assertEqual(sort_copy.name, sorter.name)
        self.assertEqual(sort_copy.img_width, 6)
        self.assertEqual(sort_copy.img_height, 5)
        self.assertEqual(sort_copy.width, 3)
        self.assertEqual(sort_copy.height, 4)
