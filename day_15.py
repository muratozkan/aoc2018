class Unit(object):

    def __init__(self, ix, t, p, ap):
        self.ix = ix
        self.t = t
        self.p = p
        self.hp = 200
        self.ap = ap

    def __lt__(self, other):
        return pos_lt(self.p, other.p)

    def __repr__(self):
        return '[%s@%s H:%d]' % (self.t, self.p, self.hp)


def pos_lt(p1, p2):
    """Compares positions, in reading order"""
    if p1[1] == p2[1]:
        return p1[0] < p2[0]
    return p1[1] < p2[1]


def find_units(dungeon):
    units = []
    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            c = dungeon[y][x]
            if c == 'G' or c == 'E':
                units.append(Unit(len(units), c, (x, y), 3))
                dungeon[y][x] = '.'

    return units


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def neighbors(pos):
    x, y = pos
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def reachable_range(dist_map, tgt_by_p, u_by_p):
    p_set = {nb for u in tgt_by_p.values() for nb in neighbors(u.p)}
    # ranges that are reachable and not occupied by another
    ranges = [(px, py) for px, py in p_set if dist_map[py][px] >= 0 and not u_by_p.get((px, py), None)]
    return ranges


def distance_map(dungeon, u_by_p, pos):
    """The distances of accessible positions from a given starting position"""
    dist_map = [[-1 for _ in line] for line in dungeon]
    edges = [pos]
    seen = {pos}
    while edges:
        cx, cy = edges.pop(0)
        dist_map[cy][cx] = min([dist_map[ny][nx] for nx, ny in neighbors((cx, cy))
                                if dist_map[ny][nx] != -1], default=-1) + 1

        nbs = [(nx, ny) for nx, ny in neighbors((cx, cy))
               if (nx, ny) not in seen and u_by_p.get((nx, ny), None) is None and dungeon[ny][nx] == '.']
        edges += nbs
        seen.update(nbs)

    return dist_map


def shortest_path(dist_map, unit, pos):
    """This algorithm is wrong. It doesn't """
    px, py = pos
    if dist_map[py][px] == -1:
        return None

    cp = pos
    path = [pos]
    paths = []
    while cp != unit.p:
        cx, cy = cp
        c_dist = dist_map[cy][cx]
        opts = [(nx, ny) for nx, ny in neighbors(cp) if c_dist > dist_map[ny][nx] != -1]
        opts.sort(key=lambda p: p[0] + 1000 * p[1])
        if len(opts) == 0:  # no more options. go back and try other branch
            if len(paths) == 0:
                # no other paths. give up.
                path = None
                break
            path = paths.pop(0)
            cp = path[-1]
        elif len(opts) == 1:  # just one option, follow it
            cp = opts[0]
            path.append(cp)
        else:  # many options. take first but save the others
            cp = opts.pop(0)
            for opt in opts:
                paths.append(path + [opt])
            path.append(cp)

    path.reverse()
    return path[1:]


def debug_print(dungeon, units, rounds):
    print('Round: %d' % rounds)
    unit_map = {u.p: u for u in units if u.hp > 0}
    for y in range(len(dungeon)):
        units = []
        for x in range(len(dungeon[0])):
            u = unit_map.get((x, y), None)
            if u:
                print(u.t, end='')
                units.append(u)
            else:
                print(dungeon[y][x], end='')

        for unit in units:
            print(' %s' % unit, end='')

        print()
    print('-----')


def target_of_attack(unit, u_by_p):
    return min([u_by_p[np] for np in neighbors(unit.p) if np in u_by_p], key=lambda u: u.hp, default=None)


def simulate_battle(dungeon, units):
    c_us = [Unit(u.ix, u.t, u.p, u.ap) for u in units]
    rounds = 0
    has_moves = True

    while has_moves:
        # debug_print(dungeon, c_us, rounds)
        c_us.sort()

        for unit in c_us:
            if unit.hp <= 0:
                continue

            # print('%s ' % unit)
            tgt_by_p = {u.p: u for u in c_us if u.hp > 0 and u.t != unit.t}  # targets of other kind
            u_by_p = {u.p: u for u in c_us if u.hp > 0 and u.ix != unit.ix}  # all alive units but me
            if len(tgt_by_p) == 0:
                has_moves = False
                break

            tgt_u = target_of_attack(unit, tgt_by_p)
            has_attacked = False
            if tgt_u is not None:
                # trivial case, am I standing next to an enemy?
                tgt_u.hp -= unit.ap
                has_attacked = True
                # print('\tAttacked %s' % tgt_u)
            else:
                # re-evaluate targets and find the nearest reachable
                dist_map = distance_map(dungeon, u_by_p, unit.p)
                range_pos_s = reachable_range(dist_map, tgt_by_p, u_by_p)  # list of points in range of targets
                range_pos_s.sort(key=lambda p: dist(unit.p, p))
                range_pos_s.sort(key=lambda ps: ps[0] + ps[1] * 1000)
                tgt_paths = []
                for tp in range_pos_s:
                    tgt_path = shortest_path(dist_map, unit, tp)
                    if tgt_path:
                        tgt_paths.append((tp, tgt_path))

                if not tgt_paths:
                    # there are targets but covered by obstacles, nothing to do
                    continue

                tgt_paths.sort(key=lambda p: len(p[1]))  # shortest path first
                unit.p = tgt_paths[0][1][0]
                # print('\tMoved to: %s' % (unit.p,))

            # attack (the unit has moved this turn)
            if not has_attacked:
                tgt_u = target_of_attack(unit, tgt_by_p)
                if tgt_u:
                    tgt_u.hp -= unit.ap
                    # print('\tAttacked %s' % tgt_u)

        if not has_moves:
            return c_us, rounds

        rounds += 1

    return None


def outcome(c_us, rounds):
    return sum([u.hp for u in c_us if u.hp > 0]) * rounds


def increase_elf_attack(units, power):
    mod_us = []
    for u in units:
        ap = u.ap if u.t == 'G' else power
        mod_us.append(Unit(u.ix, u.t, u.p, ap))
    return mod_us


def simulate_buffed_battle(dungeon, units):
    e_pow = 4
    while True:
        c_us, rounds = simulate_battle(dungeon, increase_elf_attack(units, e_pow))
        if all([u.hp > 0 for u in c_us if u.t == 'E']):
            return c_us, rounds
        else:
            e_pow += 1
            print('.')


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        dungeon = [list(x.rstrip('\n')) for x in in_file.readlines()]

    units = find_units(dungeon)
    c_us, rounds = simulate_battle(dungeon, units)
    print("Part 1: %d" % (outcome(c_us, rounds),))
    c_us, rounds = simulate_buffed_battle(dungeon, units)
    print("Part 2: %d" % (outcome(c_us, rounds),))


if __name__ == '__main__':
    main('15_input.txt')
