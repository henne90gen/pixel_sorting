
def built_in():
    return lambda pixel: pixel


def red():
    return lambda pixel: pixel[0]


def green():
    return lambda pixel: pixel[1]


def blue():
    return lambda pixel: pixel[2]


def brightness():
    return lambda pixel: pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114


def avg():
    return lambda pixel: (pixel[0] + pixel[1] + pixel[2]) / 3


# http://www.rapidtables.com/convert/color/rgb-to-hsl.htm
def hue():
    return lambda pixel: 0 if max(pixel) - min(pixel) == 0 else (
        60 * (((pixel[1] - pixel[2]) / (max(pixel) - min(pixel))) % 6) if max(pixel) == pixel[0] else (
            60 * ((pixel[2] - pixel[0]) / (max(pixel) - min(pixel)) + 2) if max(pixel) == pixel[1] else (
                60 * ((pixel[0] - pixel[1]) / (max(pixel) - min(pixel)) + 4))))


def saturation():
    return lambda pixel: 0 if max(pixel) - min(pixel) == 0 else ((max(pixel) - min(pixel)) / 255) / (
        1 - abs(((max(pixel) + min(pixel)) / 255) - 1))


def lightness():
    return lambda pixel: (max(pixel) / 255 + min(pixel) / 255) / 2


all_criteria = {"BuiltIn": built_in(), "Red": red(), "Green": green(), "Blue": blue(), "Brightness": brightness(),
                "Average": avg(), "Hue": hue(), "Saturation": saturation(), "Lightness": lightness()}
