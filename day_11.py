def power_levels(cells, serial):
    for y in range(1, 301):
        for x in range(1, 301):
            rack_id = x + 10
            pow_level = ((rack_id * y + serial) * rack_id) // 100 % 10 - 5
            cells[y - 1][x - 1] = pow_level


def grid_totals(cells, sz):
    ts = 301 - sz
    totals = [[0] * ts for _ in range(ts)]
    for ty in range(ts):
        for tx in range(ts):
            totals[ty][tx] = sum([sum(cells[yi][tx:tx + sz]) for yi in range(ty, ty + sz)])
    return max_totals(totals, sz)


def max_totals(totals, sz):
    ts = 301 - sz
    mx, my = 0, 0
    max_val = 0
    for y in range(ts):
        for x in range(ts):
            if totals[y][x] > max_val:
                max_val = totals[y][x]
                mx, my = x, y
    return mx, my, max_val


def max_total_of_size(cells):
    mx, my, m_val, ms = 0, 0, 0, 0
    for sz in range(1, 300):
        x, y, v = grid_totals(cells, sz)
        if v > m_val:
            mx, my, m_val, ms = x, y, v, sz
        print('i [%d]: (%d,%d,%d) @ %d' % (sz, mx, my, ms, m_val))
    return mx, my, ms


def main(serial):
    cells = [[0] * 300 for _ in range(300)]
    power_levels(cells, serial)
    x, y, _ = grid_totals(cells, 3)
    print("Part 1: (%d, %d)" % (x + 1, y + 1))
    x, y, s = max_total_of_size(cells)
    print("Part 2: (%d, %d) @ %d" % (x + 1, y + 1, s + 1))


if __name__ == '__main__':
    main(7803)
