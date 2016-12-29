
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

# TODO create more criteria
