EROSION_LEVELS = ['.', '=', '|']


def debug_print(cave):
    for ys in cave:
        for g in ys:
            print(EROSION_LEVELS[g], end='')
        print('')


def create_cave(depth, t_pos):
    tx, ty = t_pos
    cave = [[0] * (tx + 1) for _ in range(ty + 1)]
    cx, cy = 16807, 48271
    md = 20183

    geo_ix = [[0] * (tx + 1) for _ in range(ty + 1)]
    for y in range(ty + 1):
        for x in range(tx + 1):
            if x == 0:
                cix = (y * cy) % md
            elif y == 0:
                cix = (x * cx) % md
            else:
                ey = (geo_ix[y - 1][x] + depth) % md
                ex = (geo_ix[y][x - 1] + depth) % md
                cix = (ex * ey) % md
            geo_ix[y][x] = cix

    for y in range(ty + 1):
        for x in range(tx + 1):
            e_lvl = (geo_ix[y][x] + depth) % md
            cave[y][x] = e_lvl % 3

    return cave


def risk_level(cave, t_pos):
    tx, ty = t_pos
    return sum([sum(ys) for ys in cave]) - cave[ty][tx]


def main(depth, t_pos):
    cave = create_cave(depth, t_pos)
    print('Part 1: %d' % (risk_level(cave, t_pos),))


if __name__ == '__main__':
    main(10689, (11, 722))
    # main(510, (10, 10))
