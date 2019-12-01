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


def match_opcodes(inst_s):
    matches = []
    for reg_b, inst, reg_a in inst_s:
        c, in1, in2, out = inst
        match_insts = set()
        for op, func in OPS.items():
            reg_res = func(list(reg_b), in1, in2, out)
            if reg_res == reg_a:
                match_insts.add(op)
        matches.append((c, match_insts))
    return matches


def number_to_code(matches):
    known_codes = {}
    matches.sort(key=lambda x: len(x[1]))

    while len(known_codes) < 16:
        for c, match_is in matches:
            if len(match_is) == 0:
                continue

            for c_k, op_v in known_codes.items():
                if op_v in match_is:
                    match_is.remove(op_v)

            if len(match_is) == 1:
                known_codes[c] = list(match_is)[0]

    return known_codes


def execute(code_to_op, program):
    regs = [0, 0, 0, 0]
    for c, in1, in2, out in program:
        op = code_to_op[c]
        regs = OPS[op](regs, in1, in2, out)
    return regs


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        inst_s = []
        program = []
        before, inst = None, None
        new_lines = 0
        for line in in_file.readlines():
            if new_lines < 3:
                if line.startswith('B'):
                    before = [int(i) for i in line[9:-2].split(', ')]
                    new_lines = 0
                elif before and not inst:
                    inst = tuple([int(i) for i in line.split(' ')])
                elif inst and line.startswith('A'):
                    after = [int(i) for i in line[9:-2].split(', ')]
                    inst_s.append((before, inst, after))
                    before, inst, after = None, None, None
                elif line == '\n':
                    new_lines += 1
            else:
                inst = tuple([int(i) for i in line.split(' ')])
                program.append(inst)

    matches = match_opcodes(inst_s)
    print('Part 1: %d' % (sum([1 if len(m) >= 3 else 0 for c, m in matches]),))
    regs = execute(number_to_code(matches), program)
    print('Part 2: %d' % (regs[0],))


if __name__ == '__main__':
    main('16_input.txt')
