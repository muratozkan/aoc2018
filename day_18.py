def in_grid(x, y, x_sz, y_sz):
    return x_sz > x >= 0 and y_sz > y >= 0


def neighbor_vs(grid, pos):
    x_sz, y_sz = len(grid[0]), len(grid)
    px, py = pos
    ps = [(px + x, py + y) for x in range(-1, 2) for y in range(-1, 2)
          if (x, y) != (0, 0) and in_grid(px + x, py + y, x_sz, y_sz)]
    return [grid[y][x] for x, y in ps]


def rules(cval, nvs):
    if cval == '.':
        return '|' if sum([1 if v == '|' else 0 for v in nvs]) >= 3 else '.'
    if cval == '|':
        return '#' if sum([1 if v == '#' else 0 for v in nvs]) >= 3 else '|'
    if cval == '#':
        return '#' if sum([1 if v == '#' else 0 for v in nvs]) > 0 \
                      and sum([1 if v == '|' else 0 for v in nvs]) > 0 else '.'
    assert False


def debug_print(grid, i, of=False):
    f_out = open('18/%d.txt' % i, 'w') if of else None
    print('---', file=f_out)
    for gy in grid:
        for gc in gy:
            print(gc, end='', file=f_out)
        print('', file=f_out)
    print('', file=f_out)


def eval(grid):
    x_sz, y_sz = len(grid[0]), len(grid)
    next_grid = [['.'] * x_sz for _ in grid]
    for y in range(y_sz):
        for x in range(x_sz):
            c_val = grid[y][x]
            nvs = neighbor_vs(grid, (x, y))
            next_grid[y][x] = rules(c_val, nvs)
    return next_grid


def eval_gens(init_grid, gens):
    grid = init_grid
    for g in range(gens):
        grid = eval(grid)
        # debug_print(grid, g, True)

    return grid


def land_value(grid):
    c_ly = 0
    c_tr = 0
    for gl in grid:
        for gc in gl:
            c_ly += 1 if gc == '#' else 0
            c_tr += 1 if gc == '|' else 0
    return c_ly * c_tr


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        init_g = [list(ln.rstrip()) for ln in in_file.readlines()]

    grid = eval_gens(init_g, 10)
    l_val = land_value(grid)
    print('Part 1: %d' % (l_val,))
    grid = eval_gens(init_g, 524)
    l_val = land_value(grid)
    print('Part 2: %d' % (l_val,))


if __name__ == '__main__':
    main('18_input.txt')
