def addr(regs, in1, in2, out):
    regs[out] = regs[in1] + regs[in2]


def addi(regs, in1, in2, out):
    regs[out] = regs[in1] + in2


def mulr(regs, in1, in2, out):
    regs[out] = regs[in1] * regs[in2]


def muli(regs, in1, in2, out):
    regs[out] = regs[in1] * in2


def banr(regs, in1, in2, out):
    regs[out] = regs[in1] & regs[in2]


def bani(regs, in1, in2, out):
    regs[out] = regs[in1] & in2


def borr(regs, in1, in2, out):
    regs[out] = regs[in1] | regs[in2]


def bori(regs, in1, in2, out):
    regs[out] = regs[in1] | in2


def seti(regs, in1, in2, out):
    regs[out] = in1


def setr(regs, in1, in2, out):
    regs[out] = regs[in1]


def gtir(regs, in1, in2, out):
    regs[out] = 1 if in1 > regs[in2] else 0


def gtri(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] > in2 else 0


def gtrr(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] > regs[in2] else 0


def eqir(regs, in1, in2, out):
    regs[out] = 1 if in1 == regs[in2] else 0


def eqri(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] == in2 else 0


def eqrr(regs, in1, in2, out):
    regs[out] = 1 if regs[in1] == regs[in2] else 0


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
    print('i=%2d\t[' % (i + 1,), end='')
    for r in regs:
        print('%2d ' % (r,), end='')

    print('] %s' % (inst,))


def execute(init_regs, inst_p, program, debug_op=''):
    regs = list(init_regs)
    ip = 0
    while len(program) > ip >= 0:
        op, in1, in2, out = program[ip]

        debug_print(ip, regs, (op, in1, in2, out))
        regs[inst_p] = ip
        OPS[op](regs, in1, in2, out)
        ip = regs[inst_p] + 1

    return regs


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        ip = int(in_file.readline().rstrip().split(' ')[1])
        program = [parse(l) for l in in_file.readlines()]

    # program checks equality of reg[0] and reg[2] at line 29. The smallest number of executions is required so,
    # just set reg[0] to the value appearing on reg[2] when the program hits line 29 for the first time.

    regs = execute([10780777, 0, 0, 0, 0, 0], ip, program)
    print('Part 1: %d' % (regs[0],))
    # part 2 is in transpiled file
    # regs = execute([0, 0, 0, 0, 0, 0], ip, program, debug_op='eqrr')
    # print('Part 2: %d' % (regs[0],))


if __name__ == '__main__':
    main('21_input.txt')
