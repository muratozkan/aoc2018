def parse(in_str):
    i_s, _, ps, ss = in_str.split(' ')
    l, t = ps.split(',')
    w, h = ss.split('x')
    return int(i_s.lstrip('#')), (int(l), int(t.rstrip(':'))), (int(w), int(h))


def create_map(claims, s):
    ll = [['.'] * s for _ in range(s)]
    for i, (l, t), (ws, hs) in claims:
        for h in range(hs):
            for w in range(ws):
                c = ll[l + w][t + h]
                k = (str(i) if c is '.' else 'X')
                ll[l + w][t + h] = k
    return ll


def find_overlap(ll):
    return sum([sum([1 for c in r if c == 'X']) for r in ll])


def non_overlapping(claims, ll, s):
    claimed_areas = {}
    for i, _, (ws, hs) in claims:
        claimed_areas[i] = ws * hs

    actual_areas = {}
    for h in range(s):
        for w in range(s):
            c = ll[w][h]
            if c == '.' or c == 'X':
                continue
            a = actual_areas.get(int(c), 0)
            actual_areas[int(c)] = a + 1

    for i, a in actual_areas.items():
        if claimed_areas[i] == a:
            return i

    return None


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [parse(x) for x in in_file.readlines()]

    ll = create_map(content, 1000)
    print("Part 1: %s" % find_overlap(ll))

    print("Part 2: %s" % non_overlapping(content, ll, 1000))


if __name__ == '__main__':
    main('3_input.txt')
