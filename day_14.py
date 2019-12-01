def sequence_after(after, sz):
    ls = [0] * (after + sz + 1)
    ls[0] = 3
    ls[1] = 7
    current_sz = 2
    e1, e2 = 0, 1
    while current_sz < (after + sz):
        new_rcps = [int(c) for c in str(ls[e1] + ls[e2])]
        for i, nr in enumerate(new_rcps):
            ls[i + current_sz] = nr
        current_sz += len(new_rcps)
        e1 = (e1 + ls[e1] + 1) % current_sz
        e2 = (e2 + ls[e2] + 1) % current_sz

    return ''.join([str(i) for i in ls[after:after + sz]])


def sequence_before(inp, init_size):
    ls = [0] * init_size
    ls[0] = 3
    ls[1] = 7
    current_sz = 2
    e1, e2 = 0, 1
    in_str = str(inp)
    tgt_len = len(in_str)
    while current_sz < init_size:
        new_rcps = [int(c) for c in str(ls[e1] + ls[e2])]
        strs = set()
        for i, nr in enumerate(new_rcps):
            ls[i + current_sz] = nr
            st_i = i + current_sz - tgt_len
            if st_i >= 0:
                strs.add(''.join([str(i) for i in ls[st_i:st_i + tgt_len]]))

        if in_str in strs:
            return current_sz - tgt_len

        current_sz += len(new_rcps)
        e1 = (e1 + ls[e1] + 1) % current_sz
        e2 = (e2 + ls[e2] + 1) % current_sz

    return -1


def main():
    # print('Part 1: %s' % (sequence_after(864801, 10),))
    print('Part 2: %s' % (sequence_before(864801, 1000000000),))  # one less than correct answer for some reason?


if __name__ == '__main__':
    main()
