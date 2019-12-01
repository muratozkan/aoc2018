def parse(line):
    a_str, range_str = line.split(', ')
    range_min, range_max = range_str.split('..')
    return a_str[0], int(a_str[2:]), int(range_min[2:]), int(range_max)


def xy_range(sd_s):
    xmin, xmax, ymin, ymax = 10000, 0, 10000, 0
    for xy, a, bn, bx in sd_s:
        if xy == 'x':
            xmin = min(a, xmin)
            xmax = max(a, xmax)
            ymax = max(bx, ymax)
            ymin = min(bn, ymin)
        else:
            xmin = min(bn, xmin)
            xmax = max(bx, xmax)
            ymax = max(a, ymax)
            ymin = min(a, ymin)
    return xmin, xmax, ymin, ymax


def make_grid(sd_s):
    xmin, xmax, ymin, ymax = xy_range(sd_s)
    x_size = xmax - xmin + 3
    y_size = ymax - ymin + 1
    grid = [['.'] * x_size for _ in range(y_size)]
    for xy, a, bn, bx in sd_s:
        points = [(a, b) for b in range(bn, bx + 1)]
        if xy == 'y':
            points = [(pb, pa) for pa, pb in points]
        for px, py in points:
            grid[py - ymin][px - xmin + 1] = '#'
    grid[0][501 - xmin] = '|'
    return grid, (501 - xmin, 0)


P_UP = (0, -1)
P_DOWN = (0, 1)
P_LEFT = (-1, 0)
P_RIGHT = (1, 0)


def neighbor(pos, dir_p):
    return pos[0] + dir_p[0], pos[1] + dir_p[1]


def in_grid(p, xy_size):
    px, py = p
    mx, my = xy_size
    return 0 <= px < mx and 0 <= py < my


def debug_print(grid, i, file_out=False):
    df = open('17/%d.txt' % i, 'w') if file_out else None
    print('i: %d---' % i, file=df)
    for gy in grid:
        for gc in gy:
            print(gc, end='', file=df)
        print('', file=df)

    if file_out:
        df.close()


def water_flow(grid, source_pos):
    xy_size = len(grid[0]), len(grid)
    eval_q = [source_pos]
    processed = set()
    i = 0
    while eval_q:
        # debug_print(grid, i)
        ep = eval_q.pop(0)
        # can go down?
        nd_p = neighbor(ep, P_DOWN)
        if not in_grid(nd_p, xy_size) or nd_p in processed:  # bottom edge, flows down infinitely
            processed.add(ep)
            i += 1
            continue

        nd_x, nd_y = nd_p
        if grid[nd_y][nd_x] == '.':
            grid[nd_y][nd_x] = '|'
            eval_q.insert(0, ep)
            eval_q.insert(0, nd_p)
        elif grid[nd_y][nd_x] == '|':
            if not eval_q or eval_q[0][1] != nd_y:  # there's a pool below
                ps = []
                is_unbounded = False
                for sx in range(nd_x, -1, -1):
                    if grid[nd_y][sx] == '|':
                        ps.append((sx, nd_y))
                    elif grid[nd_y][sx] == '.':
                        is_unbounded = True
                        ps.clear()
                        break
                    elif grid[nd_y][sx] == '#':
                        break

                if not is_unbounded:
                    for sx in range(nd_x, xy_size[0]):
                        if grid[nd_y][sx] == '|':
                            ps.append((sx, nd_y))
                        elif grid[nd_y][sx] == '.':
                            ps.clear()
                            break
                        elif grid[nd_y][sx] == '#':
                            break

                for px, py in ps:
                    if in_grid((px, py + 1), xy_size) and grid[py + 1][px] == '|' or grid[py + 1][px] == '.':
                        ps.clear()
                        break

                for px, py in ps:
                    grid[py][px] = '~'

        if grid[nd_y][nd_x] == '#' or grid[nd_y][nd_x] == '~':  # found clay. check right and left
            n_lr_ps = [neighbor(ep, P_LEFT), neighbor(ep, P_RIGHT)]
            for nx, ny in n_lr_ps:
                if in_grid((nx, ny), xy_size) and grid[ny][nx] == '.':
                    grid[ny][nx] = '|'
                    eval_q.insert(0, (nx, ny))
        i += 1


def count_water(grid):
    return sum([sum([1 if x == '|' or x == '~' else 0 for x in xs]) for xs in grid])


def count_still(grid):
    return sum([sum([1 if x == '~' else 0 for x in xs]) for xs in grid])


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        scan_data = [parse(l) for l in in_file.readlines()]

    grid, sp = make_grid(scan_data)
    water_flow(grid, sp)
    print('Part 1: %d' % (count_water(grid),))
    print('Part 2: %d' % (count_still(grid),))


if __name__ == '__main__':
    main('17_input.txt')
