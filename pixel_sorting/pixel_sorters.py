import math

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.helper import get_pixels


class PixelSorter(object):
    def __init__(self, name, img_width=0, img_height=0, sort_criteria=sort_criteria.built_in(), reverse=False):
        self.name = name
        self.img_width = img_width
        self.img_height = img_height
        self.sort_criteria = sort_criteria
        self.reverse = reverse

    def to_string(self):
        return self.name

    def sort_pixels(self, pixels):
        pass

    def sort_image(self, img):
        return self.sort_pixels(get_pixels(img))


class BasicSorter(PixelSorter):
    def __init__(self, sort_criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("BasicSorter", sort_criteria=sort_criteria, reverse=reverse)

    def sort_pixels(self, pixels):
        pixels.sort(key=self.sort_criteria, reverse=self.reverse)
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__("Inverter")

    def sort_pixels(self, pixels):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels


class RowSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, row, reverse=False):
        super().__init__("RowSorter", img_width, img_height, sort_criteria, reverse)
        self.row = row

    def sort_pixels(self, pixels):
        sorting = []
        for col in range(self.img_width):
            sorting.append(pixels[self.row * self.img_width + col])

        sorting.sort(key=self.sort_criteria, reverse=self.reverse)

        index = 0
        for col in range(self.img_width):
            pixels[self.row * self.img_width + col] = sorting[index]
            index += 1
        return pixels


class AlternatingRowSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, sort_criteria=sort_criteria.built_in(), reverse=False, alternation=1):
        super().__init__("AlternatingRowSorter", img_width, img_height, sort_criteria, reverse)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_height):
            row_sorter = RowSorter(self.img_width, self.img_height, self.sort_criteria, i, reverse)
            row_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class ColumnSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, column, reverse=False):
        super().__init__("ColumnSorter", img_width, img_height, sort_criteria, reverse)
        self.column = column

    def sort_pixels(self, pixels):
        sorting = []
        for row in range(self.img_height):
            sorting.append(pixels[row * self.img_width + self.column])

        sorting.sort(key=self.sort_criteria, reverse=self.reverse)

        index = 0
        for row in range(self.img_height):
            pixels[row * self.img_width + self.column] = sorting[index]
            index += 1
        return pixels


class AlternatingColumnSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, sort_criteria=sort_criteria.built_in(), reverse=False, alternation=1):
        super().__init__("AlternatingColumnSorter", img_width, img_height, sort_criteria, reverse)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_width):
            column_sorter = ColumnSorter(self.img_width, self.img_height, self.sort_criteria, i, reverse)
            pixels = column_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class DiamondSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, sort_criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("DiamondSorter", img_width, img_height, sort_criteria, reverse)
        self.x = 0
        self.y = 0

    def next_position(self, pos):
        x = pos[0]
        y = pos[1]
        if x == 0 and y == 0:
            return 1, 0
        angle = math.atan2(y, x)
        if 0 <= angle < math.pi / 2:
            x -= 1
            y += 1
        elif math.pi / 2 <= angle < math.pi:
            x -= 1
            y -= 1
        elif -math.pi <= angle < -math.pi / 2 or angle == math.pi:
            x += 1
            y -= 1
        elif -math.pi / 2 <= angle < 0:
            x += 1
            y += 1
        if y == 0 and x >= 0:
            x += 1
        pos = (x, y)
        return pos

    def sort_pixels(self, pixels):
        self.x = round(self.img_width / 2)
        self.y = round(self.img_height / 2)

        pixels.sort(key=self.sort_criteria, reverse=self.reverse)

        temp_pixels = [p for p in pixels]
        index = 0
        pos = (0, 0)
        while True:
            real_x = pos[0] + self.x
            real_y = pos[1] + self.y
            if index >= len(temp_pixels):
                break
            if 0 <= real_x < self.img_width and 0 <= real_y < self.img_height:
                pixels[real_y * self.img_width + real_x] = temp_pixels[index]
                index += 1
            pos = self.next_position(pos)
        return pixels


class CircleSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, sort_criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("CircleSorter", img_width, img_height, sort_criteria, reverse)
        self.x = int(self.img_width / 2)
        self.y = int(self.img_height / 2)
        self.max_radius = math.sqrt(self.x * self.x + self.y * self.y)

    def draw_pixel(self, pixels, temp_pixels, index, x, y):
        real_x = self.x + x
        real_y = self.y + y
        if real_x < 0 or real_y < 0:
            return 0
        if real_x >= self.img_width or real_y >= self.img_height:
            return 0
        if 0 <= index < len(temp_pixels):
            pixels[self.img_width * real_y + real_x] = temp_pixels[index]
            return 1
        return 0

    def draw_octant_pixels(self, pixels, temp_pixels, index, x, y):
        index += self.draw_pixel(pixels, temp_pixels, index, x, y)
        index += self.draw_pixel(pixels, temp_pixels, index, -x, y)
        if y != 0:
            index += self.draw_pixel(pixels, temp_pixels, index, -x, -y)
            index += self.draw_pixel(pixels, temp_pixels, index, x, -y)
        if not x == y:
            index += self.draw_pixel(pixels, temp_pixels, index, y, x)
            index += self.draw_pixel(pixels, temp_pixels, index, y, -x)
            if y != 0:
                index += self.draw_pixel(pixels, temp_pixels, index, -y, x)
                index += self.draw_pixel(pixels, temp_pixels, index, -y, -x)
        return index

    def draw_circle(self, pixels, temp_pixels, pixel_set, index, radius):
        rad_sq = radius * radius
        cur_x = int(radius)
        cur_y = 0
        while True:
            if cur_y < len(pixel_set) and cur_x < len(pixel_set[cur_y]) and not pixel_set[cur_y][cur_x]:
                index = self.draw_octant_pixels(pixels, temp_pixels, index, cur_x, cur_y)
                pixel_set[cur_y][cur_x] = True
            cur_y += 1
            new_x1 = cur_x
            new_x2 = cur_x - 1
            dist1 = cur_y * cur_y + new_x1 * new_x1
            dist2 = cur_y * cur_y + new_x2 * new_x2
            if abs(dist1 - rad_sq) <= abs(dist2 - rad_sq):
                cur_x = new_x1
            else:
                cur_x = new_x2
            angle = math.atan2(cur_y, cur_x)
            if angle > math.pi / 4:
                break
        return index

    def sort_pixels(self, pixels):
        self.x = int(self.img_width / 2)
        self.y = int(self.img_height / 2)
        self.max_radius = math.sqrt(self.x * self.x + self.y * self.y)
        pixels.sort(key=self.sort_criteria, reverse=self.reverse)
        temp_pixels = [p for p in pixels]

        pixel_set = []
        x_offset = 0
        y_offset = 0
        if self.img_width % 2 != 0:
            x_offset = 1
        if self.img_height % 2 != 0:
            y_offset = 1
        for i in range(self.y + y_offset):
            temp = [False for _ in range(self.x + x_offset)]
            pixel_set.append(temp)

        radius = 1
        index = 1
        self.draw_pixel(pixels, temp_pixels, 0, 0, 0)
        while radius <= self.max_radius + 1:
            index = self.draw_circle(pixels, temp_pixels, pixel_set, index, radius)
            radius += 0.5

        return pixels
