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


def abs_min(list_of_candidates):
    list_of_absolutes = []
    for each in list_of_candidates:
        list_of_absolutes.append(abs(each))

    minimum = min(list_of_absolutes)
    position = list_of_absolutes.index(minimum)
    true_minimum = list_of_candidates[position]
    return true_minimum


def abs_min_old(*items):
    best = abs(items[0])
    best_actual = items[0]

    for item in items:
        if abs(item) < best:
            best = abs(item)
            best_actual = item


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
        change_x = abs_min([change_x, x_dist])
    if y_dist == 0:
        change_y = 0
    else:
        change_y = y_dist / factor
        change_y = round(change_y)
        change_y = abs_min([change_y, y_dist])

    return (change_x, change_y)
