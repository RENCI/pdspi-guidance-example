from random import seed, random


def _get_random(min_num, max_num):
    return random() * (max_num - min_num) + min_num


def generate_time_series_data(n):
    data = []
    seed(1)
    for i in range(n):
        if i == 0:
            y = _get_random(0, 1)
        else:
            y = max(data[i-1]['y'] + _get_random(-1, 1), 0)
        data.append({
            'x': i,
            'y': y
        })

    return data


def generate_multi_time_series_data(n, m):
    data = []
    seed(1)
    for i in range(m):
        group = 'group {}'.format(i)
        for j in range(n):
            if j == 0:
                y = _get_random(0, 1)
            else:
                y = max(data[len(data) - 1]['y'] + _get_random(-1, 1), 0)
            data.append({
                'x': j,
                'y': y,
                'group': group
            })
    return data


def generate_scatter_plot_data(n):
    data = []
    seed(1)
    a = _get_random(-1, 1)
    b = _get_random(0, 1)

    for i in range(n):
        x = _get_random(-1, 1)
        y = x * a + _get_random(0, b)
        data.append({'x': x, 'y': y})

    return data


def generate_multi_scatter_plot_data(n, m):
    data = []
    seed(1)
    for i in range(m):
        group = 'group {}'.format(i)
        a = _get_random(-1, 1)
        b = _get_random(0, 1)
        for j in range(n):
            x = _get_random(-1, 1)
            y = x * a + _get_random(0, b)
            data.append({
                'x': x,
                'y': y,
                'group': group
            })
    return data


def generate_histogram_data(n):
    data = []
    seed(1)
    for i in range(n):
        x = round(_get_random(1, 10))
        data.append({
            'x': x
        })
    return data
