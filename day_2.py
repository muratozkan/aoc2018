

def freq_letter(id):
    letters = {}
    for ch in id:
        c = letters.get(ch, 0)
        letters[ch] = c + 1

    freqs = {}
    for (k, v) in letters.items():
        lc = freqs.get(v, 0)
        freqs[v] = lc + 1

    return freqs


def checksum(ids):
    twos = 0
    thrs = 0
    for id in ids:
        freq = freq_letter(id)
        twos += 1 if freq.get(2, 0) >= 1 else 0
        thrs += 1 if freq.get(3, 0) >= 1 else 0

    return twos * thrs


def id_similarity(id_1, id_2):
    s = 0
    for i in range(len(id_1)):
        s += 1 if id_1[i] == id_2[i] else 0
    return s


def decode(id_1, id_2):
    s = []
    for i in range(len(id_1)):
        if id_1[i] == id_2[i]:
            s.append(id_1[i])

    return ''.join(s)


def closest_ids(ids):
    max_s = 0
    max_ids = None
    for x in range(len(ids)):
        for y in range(len(ids)):
            if x == y:
                continue

            id1, id2 = ids[x], ids[y]
            s = id_similarity(id1, id2)
            if s > max_s:
                max_s = s
                max_ids = (id1, id2)

    return decode(*max_ids)


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [x.strip() for x in in_file.readlines()]

    print("Part 1: %s" % checksum(content))

    print("Part 2: %s" % closest_ids(content))


if __name__ == '__main__':
    main('2_input.txt')
