import math
import


class PixelSorter(object):
    def __init__(self, img_width=0, img_height=0, sort_criteria=SortCriteria.built_in()):
        self.img_width = img_width
        self.img_height = img_height
        self.sort_criteria = sort_criteria

    def sort_pixels(self, pixels):
        pass

    def sort_image(self, img):
        return self.sort_pixels(get_pixels(img))


class BasicSorter(PixelSorter):
    def __init__(self, sort_criteria):
        super().__init__(sort_criteria=sort_criteria)

    def sort_pixels(self, pixels):
        pixels.sort(key=self.sort_criteria)
        return pixels


class Inverter(PixelSorter):
    def __init__(self):
        super().__init__()

    def sort_pixels(self, pixels):
        for i in range(len(pixels)):
            r = 255 - pixels[i][0]
            g = 255 - pixels[i][1]
            b = 255 - pixels[i][2]
            pixels[i] = (r, g, b)
        return pixels


class RowSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria, row, reverse=False):
        super().__init__(img_width, img_height, sort_criteria)
        self.row = row
        self.reverse = reverse

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
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
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
        super().__init__(img_width, img_height, sort_criteria)
        self.column = column
        self.reverse = reverse

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
    def __init__(self, img_width, img_height, sort_criteria, alternation):
        super().__init__(img_width, img_height, sort_criteria)
        self.alternation = alternation

    def sort_pixels(self, pixels):
        reverse = False
        for i in range(self.img_width):
            column_sorter = ColumnSorter(self.img_width, self.img_height, self.sort_criteria, i, reverse)
            pixels = column_sorter.sort_pixels(pixels)
            if i % self.alternation == 0:
                reverse = not reverse
        return pixels


class CircleSorter(PixelSorter):
    def __init__(self, img_width, img_height, sort_criteria):
        super().__init__(img_width, img_height, sort_criteria)
        self.x = int(img_width / 2)
        self.y = int(img_height / 2)
        self.max_radius = math.sqrt(self.x * self.x + self.y * self.y)

    def sort_pixels(self, pixels):
        pixels.sort(key=self.sort_criteria, reverse=True)

        temp_pixels = [p for p in pixels]
        index = 0
        pixels[self.y * self.img_width + self.x] = temp_pixels[index]
        x = 1
        y = 0
        while True:
            angle = math.atan2(y, x)
            print("Angle:", angle, "X:", x, "Y:", y)
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
            real_x = x + self.x
            real_y = y + self.y
            radius = math.sqrt(x * x + y * y)
            if radius > self.max_radius:
                break
            if 0 <= real_x < self.img_width and 0 <= real_y < self.img_height and index + 1 < len(temp_pixels):
                index += 1
                print(index)
                pixels[real_y * self.img_width + real_x] = temp_pixels[index]

        return pixels
