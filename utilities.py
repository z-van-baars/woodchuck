import math

logging_on = True


def log(*args, **kwargs):
    if logging_on:
        print(*args, **kwargs)


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def get_vector(self, a, b, x, y):
    distance_to_target = distance(a, b, x, y)
    factor = distance_to_target / self.speed
    x_dist = a - x
    y_dist = b - y
    if x_dist == 0:
        change_x = 0
    else:
        change_x = x_dist / factor
        change_x = round(change_x)
    if y_dist == 0:
        change_y = 0
    else:
        change_y = y_dist / factor
        change_y = round(change_y)

    return (change_x, change_y)
