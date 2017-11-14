import math

import sort_criteria
from sorters.basic import PixelSorter


class CircleSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("CircleSorter", img_width, img_height, criteria, reverse)
        self.x = int(self.img_width / 2)
        self.y = int(self.img_height / 2)
        self.max_radius = math.sqrt(self.x * self.x + self.y * self.y)

    def copy(self):
        return CircleSorter(self.img_width, self.img_height, self.criteria, self.reverse)

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
        pixels.sort(key=self.criteria, reverse=self.reverse)
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
