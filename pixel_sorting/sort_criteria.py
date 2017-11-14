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
    """
    :return: 0-360 degrees from the color circle
    """
    return lambda pixel: 0 if max(pixel) - min(pixel) == 0 else (
        60 * (((pixel[1] - pixel[2]) / (max(pixel) - min(pixel))) % 6) if max(pixel) == pixel[0] else (
            60 * ((pixel[2] - pixel[0]) / (max(pixel) - min(pixel)) + 2) if max(pixel) == pixel[1] else (
                60 * ((pixel[0] - pixel[1]) / (max(pixel) - min(pixel)) + 4))))


def saturation():
    """
    Percentage of full saturation
    :return: ranging from 0 to 1
    """
    return lambda pixel: 0 if max(pixel) - min(pixel) == 0 else ((max(pixel) - min(pixel)) / 255) / (
        1 - abs(((max(pixel) + min(pixel)) / 255) - 1))


def lightness():
    """
    Percentage of full lightness
    :return: ranging from 0 to 1
    """
    return lambda pixel: (max(pixel) / 255 + min(pixel) / 255) / 2


def threshold(criteria, num):
    """
    :param criteria: sort criteria that we want to use
    :param num: number above which the criteria is going to be used
    :return: result of criteria or 0
    """
    if type(criteria((0, 0, 0))) is tuple:
        return lambda pixel: pixel
    return lambda pixel: criteria(pixel) if criteria(pixel) > num else 0


def get_half_threshold(crit_str):
    if crit_str == "Red" or crit_str == "Green" or crit_str == "Blue" or crit_str == "Average" or crit_str == "Brightness":
        return 256 / 2
    elif crit_str == "Hue":
        return 360 / 2
    elif crit_str == "Saturation" or crit_str == "Lightness":
        return 1 / 2
    else:
        return 0


all_criteria = {"BuiltIn": built_in(), "Red": red(), "Green": green(), "Blue": blue(), "Brightness": brightness(),
                "Average": avg(), "Hue": hue(), "Saturation": saturation(), "Lightness": lightness()}
thresholds = {}
for crit in all_criteria:
    thresholds["HalfThreshold" + crit] = threshold(all_criteria[crit], get_half_threshold(crit))
all_criteria.update(thresholds)
