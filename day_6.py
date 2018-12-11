def parse(in_str):
    x, y = in_str.split(', ')
    return int(x), int(y)


def bounding_points(points):
    assert len(points) > 4
    p_nw = (1000, 1000)
    p_se = (-1000, -1000)
    for p in points:
        if p_nw[0] > p[0]:
            p_nw = p[0], p_nw[1]

        if p_nw[1] > p[1]:
            p_nw = p_nw[0], p[1]

        if p_se[0] < p[0]:
            p_se = p[0], p_se[1]

        if p_se[1] < p[1]:
            p_se = p_se[0], p[1]

    return p_nw, p_se


def debug_print(m):
    for y in range(len(m[0])):
        for x in range(len(m)):
            i, d = m[x][y]
            c = '.'
            if i is not None:
                c = chr(ord('a') + i)
                c = c.upper() if d == 0 else c
            print(c, end='')
        print('')


def areas(p_nw, p_se, points):
    w = p_se[0] - p_nw[0] + 1
    h = p_se[1] - p_nw[1] + 1

    m = [[None] * h for _ in range(w)]
    for i, (px, py) in enumerate(points):
        ax, ay = (px - p_nw[0]), (py - p_nw[1])
        m[ax][ay] = (i, 0)
        for x in range(w):
            for y in range(h):
                np = m[x][y]
                man_dist = abs(x - ax) + abs(y - ay)
                if np is None:
                    m[x][y] = i, man_dist
                elif np[1] != 0:
                    if man_dist < np[1]:
                        m[x][y] = i, man_dist
                    elif man_dist == np[1]:
                        m[x][y] = None, man_dist

    return m


def area_per_point(m):
    area = {}
    h = len(m[0]) - 1
    w = len(m) - 1
    for y in range(h + 1):
        for x in range(w + 1):
            i, d = m[x][y]
            if i is not None:
                a = area.get(i, 0)
                if a == -1:
                    continue

                if x == 0 or y == 0 or x == w or y == h:
                    a = -1
                else:
                    a += 1

                area[i] = a
    return area


def enclosed_areas(points):
    p_nw, p_se = bounding_points(points)
    m = areas(p_nw, p_se, points)
    # debug_print(m)
    return max(area_per_point(m).items(), key=lambda x: x[1])[1]


def middle_area(points, less_than):
    p_nw, p_se = bounding_points(points)

    w = p_se[0] - p_nw[0] + 1
    h = p_se[1] - p_nw[1] + 1

    count = 0
    for x in range(w):
        for y in range(h):
            p_d = 0
            for px, py in points:
                ax, ay = (px - p_nw[0]), (py - p_nw[1])
                p_d += abs(x - ax) + abs(y - ay)

            count += 1 if p_d < less_than else 0

    return count


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [parse(x) for x in in_file.readlines()]

    # print("Part 1: %s" % (enclosed_areas(content)))
    middle_area(content, 10000)
    pass


if __name__ == '__main__':
    main('6_input.txt')
