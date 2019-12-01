def addr(regs, in1, in2, out):
    regs[out] = regs[in1] + regs[in2]
    return regs


def addi(regs, in1, in2, out):
    regs[out] = regs[in1] + in2
    return regs


def mulr(regs, in1, in2, out):
    regs[out] = regs[in1] * regs[in2]
    return regs


def muli(regs, in1, in2, out):
    regs[out] = regs[in1] * in2
    return regs


def banr(regs, in1, in2, out):
    regs[out] = regs[in1] & regs[in2]
    return regs


def bani(regs, in1, in2, out):
    regs[out] = regs[in1] & in2
    return regs


def borr(regs, in1, in2, out):
    regs[out] = regs[in1] | regs[in2]
    return regs


def bori(regs, in1, in2, out):
    regs[out] = regs[in1] | in2
    return regs


def seti(regs, in1, in2, out):
    regs[out] = in1
    return regs


def setr(regs, in1, in2, out):
    regs[out] = regs[in1]
    return regs


def gtir(regs, in1, in2, out):
    regs[out] = 1 if in1 > regs[in2] else 0
    return regs


def gtri(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] > in2 else 0
    return regs


def gtrr(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] > regs[in2] else 0
    return regs


def eqir(regs, in1, in2, out):
    regs[out] = 1 if in1 == regs[in2] else 0
    return regs


def eqri(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] == in2 else 0
    return regs


def eqrr(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] == regs[in2] else 0
    return regs


OPS = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def parse(line):
    op, in1, in2, out = line.rstrip().split(' ')
    return op, int(in1), int(in2), int(out)


def debug_print(i, regs, inst):
    print('i=%2d\t[' % (i,), end='')
    for r in regs:
        print('%2d ' % (r,), end='')

    print('] %s' % (inst,))


def execute(init_regs, inst_p, program):
    regs = list(init_regs)
    ip = 0

    while len(program) > ip >= 0:
        op, in1, in2, out = program[ip]

        debug_print(ip, regs, (op, in1, in2, out))
        regs[inst_p] = ip
        regs = OPS[op](regs, in1, in2, out)
        ip = regs[inst_p] + 1

    return regs


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        ip = int(in_file.readline().rstrip().split(' ')[1])
        program = [parse(l) for l in in_file.readlines()]

    # regs = execute([0, 0, 0, 0, 0, 0], ip, program)
    # print('Part 1: %d' % (regs[0],))
    regs = execute([1, 0, 0, 0, 0, 0], ip, program)
    print('Part 2: %d' % (regs[0],))    # answer is 14_068_560, sum of all factors of 10_551_417


if __name__ == '__main__':
    main('19_input.txt')
