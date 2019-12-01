def parse(line):
    pos_str, vel_str = line.rstrip().split('> ')
    px, py = pos_str[10:].split(', ')
    vx, vy = vel_str[10:-1].split(', ')
    return (int(px), int(py)), (int(vx), int(vy))


def point_bounds(ps):
    px_max, py_max = -100000, -100000
    px_min, py_min = 100000, 100000
    for px, py in ps:
        if px > px_max:
            px_max = px

        if px < px_min:
            px_min = px

        if py > py_max:
            py_max = py

        if py < py_min:
            py_min = py

    return (py_max, py_min), (px_max, px_min)


def print_points(i, points, bounds):
    (py_max, py_min), (px_max, px_min) = bounds

    ps_set = set(points)

    with open('10/%d.out' % (i,), 'w') as out_file:
        for y in range(py_min, py_max + 1):
            for x in range(px_min, px_max + 1):
                out_file.write('#' if (x, y) in ps_set else '.')
            out_file.write('\n')


def move(points, vs):
    return [(px + vx, py + vy) for (px, py), (vx, vy) in zip(points, vs)]


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        points = [parse(line) for line in in_file.readlines()]

    ps, vs = [], []
    for (px, py), v in points:
        ps.append((px, py))
        vs.append(v)

    py, px = point_bounds(ps)
    i = 0
    while i < 12000:
        print("i: %d" % (i,))
        if py[0] - py[1] < 20:
            print_points(i, ps, (py, px))

        ps = move(ps, vs)
        py, px = point_bounds(ps)
        i += 1


if __name__ == '__main__':
    main('10_input.txt')
