

def solve(freqs):
    seen_freq = set()
    seen_freq.add(0)
    found = None
    i = 0
    f = 0
    while found is None:
        r_i = i % len(freqs)
        f += freqs[r_i]
        if f in seen_freq:
            found = f

        seen_freq.add(f)
        i += 1

    return found


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [int(x.strip()) for x in in_file.readlines()]

    print("Part 1: %s" % sum(content))

    # print(solve([1, -1]))
    # print(solve([+3, +3, +4, -2, -4]))
    # print(solve([-6, +3, +8, +5, -6]))
    # print(solve([+7, +7, -2, -7, -4]))
    print("Part 2: %s" % solve(content))


if __name__ == '__main__':
    main('1_input.txt')
