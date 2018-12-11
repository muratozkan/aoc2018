def reacts(a, b):
    return a.lower() == b.lower() and a != b


def collapse(from_in, ignored=None):
    in_l = from_in
    if ignored:
        in_l = list(filter(lambda x: x.lower() != ignored, from_in))

    size = len(in_l)
    out_l = [in_l[0]]
    for i in range(0, size):
        if out_l and reacts(in_l[i], out_l[-1]):
            out_l.pop()
        else:
            out_l.append(in_l[i])

    return out_l


def problematic(in_l):
    cs = set()
    for c in in_l:
        if c.lower() not in cs:
            cs.update(c.lower())

    best = [(c, len(collapse(in_l, ignored=c))) for c in cs]
    best.sort(key=lambda x: x[1])
    return best[0]


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = in_file.readline().strip('\n')

    print("Part 1: %s" % len(collapse(list(content))))
    print("Part 2: %s" % (problematic(list(content)),))


if __name__ == '__main__':
    main('5_input.txt')
