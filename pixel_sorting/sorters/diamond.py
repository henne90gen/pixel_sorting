import math
from pixel_sorting.sorters.basic import PixelSorter


class DiamondSorter(PixelSorter):
    def __init__(self, reverse=False):
        super().__init__("DiamondSorter", reverse)

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

    def sort_pixels(self, pixels, img_width, img_height, criteria):
        x = round(img_width / 2)
        y = round(img_height / 2)

        pixels.sort(key=criteria, reverse=self.reverse)

        temp_pixels = [p for p in pixels]
        index = 0
        pos = (0, 0)
        while True:
            real_x = pos[0] + x
            real_y = pos[1] + y
            if index >= len(temp_pixels):
                break
            if 0 <= real_x < img_width and 0 <= real_y < img_height:
                pixels[real_y * img_width + real_x] = temp_pixels[index]
                index += 1
            pos = self.next_position(pos)
        return pixels
