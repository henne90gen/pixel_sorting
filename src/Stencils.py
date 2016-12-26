import math
from src.helper import *


class Stencil(object):
    def __init__(self, img_width, img_height, x, y):
        self.img_width = img_width
        self.img_height = img_height
        self.x = x
        self.y = y

    def cut_out_pixels(self, pixels):
        pass

    def cut_out_image(self, img):
        return self.cut_out_pixels(get_pixels(img))

    def put_in_pixels(self, pixels, rect_pixels):
        pass

    def put_in_image(self, img, rect_pixels):
        self.img_width = img.size[0]
        self.img_height = img.size[1]
        return self.put_in_pixels(get_pixels(img), rect_pixels)


class RectangleStencil(Stencil):
    def __init__(self, img_width, img_height, x, y, width, height):
        super().__init__(img_width, img_height, x, y)
        self.width = width
        self.height = height

    def cut_out_pixels(self, pixels):
        result = []
        local_width = self.width
        local_height = self.height
        if self.y + local_height > self.img_height:
            local_height = self.img_height - self.y
        if self.x + local_width > self.img_width:
            local_width = self.img_width - self.x
        if self.y >= self.img_height or self.x >= self.img_width:
            raise Exception("Position out of bounds")

        for row in range(self.y, self.y + local_height):
            for col in range(self.x, self.x + local_width):
                result.append(pixels[row * self.img_width + col])
        return result

    def put_in_pixels(self, pixels, rect_pixels):
        index = 0
        for row in range(self.y, self.y + self.height):
            for col in range(self.x, self.x + self.width):
                pixels[row * self.img_width + col] = rect_pixels[index]
                index += 1
        return pixels


class CircleStencil(Stencil):
    def __init__(self, img_width, img_height, x, y, radius):
        super().__init__(img_width, img_height, x, y)
        self.radius = radius

    def cut_out_pixels(self, pixels):
        result = []
        begin = int(self.y - self.radius)
        end = int(self.y + self.radius)
        for row in range(begin, end + 1):
            angle = 0
            if row < self.y:
                if row == begin:
                    angle = math.pi / 2
                else:
                    angle = math.asin((self.y - row) / self.radius)
            if row > self.y:
                if row == end:
                    angle = math.pi / 2
                else:
                    angle = math.asin((row - self.y) / self.radius)
            cathetus = int(math.cos(angle) * self.radius)
            begin = self.x - cathetus
            end = self.x + cathetus
            for col in range(begin, end + 1):
                result.append(pixels[row * self.img_width + col])
        return result

    def put_in_pixels(self, pixels, rect_pixels):
        index = 0
        begin = int(self.y - self.radius)
        end = int(self.y + self.radius)
        for row in range(begin, end + 1):
            angle = 0
            if row < self.y:
                if row == begin:
                    angle = math.pi / 2
                else:
                    angle = math.asin((self.y - row) / self.radius)
            if row > self.y:
                if row == end:
                    angle = math.pi / 2
                else:
                    angle = math.asin((row - self.y) / self.radius)
            cathetus = int(math.cos(angle) * self.radius)
            begin = self.x - cathetus
            end = self.x + cathetus
            for col in range(begin, end + 1):
                pixels[row * self.img_width + col] = rect_pixels[index]
                index += 1
        return pixels
