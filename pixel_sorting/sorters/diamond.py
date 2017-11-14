import math

import pixel_sorting.sort_criteria as sort_criteria
from pixel_sorting.sorters.basic import PixelSorter


class DiamondSorter(PixelSorter):
    def __init__(self, img_width=0, img_height=0, criteria=sort_criteria.built_in(), reverse=False):
        super().__init__("DiamondSorter", img_width, img_height, criteria, reverse)
        self.x = 0
        self.y = 0

    def copy(self):
        return DiamondSorter(self.img_width, self.img_height, self.criteria, self.reverse)

    @staticmethod
    def next_position(pos):
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

        pixels.sort(key=self.criteria, reverse=self.reverse)

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
