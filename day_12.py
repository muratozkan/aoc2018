class LLNode(object):

    def __init__(self, i, p):
        self.i = i
        self.p = p
        self.right = None

    def add_right(self, node):
        assert self.right is None
        self.right = node
        return self


def right_or_false(node):
    return node.right.p if node and node.right else False


def parse_rule(rl):
    cond, oc = rl.rstrip().split(' => ')
    return tuple([c == '#' for c in cond]), oc == '#'


def parse_state(st_str):
    head = None
    prev = None

    for i, s in enumerate(st_str):
        node = LLNode(i, s == '#')
        if head is None:
            head = node
        else:
            prev.add_right(node)
        prev = node

    if prev.p:
        prev.add_right(LLNode(prev.i + 1, False).add_right(LLNode(prev.i + 2, False)))

    return head


def debug_print(head, gen):
    print("[%3d] [H:%d]  " % (gen, head.i), end='')
    current = head
    while current is not None:
        print('#' if current.p else '.', end='')
        current = current.right

    print('')


def count_pots(head):
    c = 0
    current = head
    while current is not None:
        c += current.i if current.p else 0
        current = current.right

    return c


def extrapolate_repeating(totals, num_deltas, total_gens):
    deltas = []
    prev = 0
    rep_ix = -1
    for i, t in enumerate(totals):
        d = t - prev
        if deltas and all([d == dt for dt in deltas]):
            rep_ix = i - num_deltas
            break

        if len(deltas) == num_deltas:
            deltas.pop(0)
        prev = t
        deltas.append(d)

    return (total_gens - rep_ix) * deltas[0] + totals[rep_ix]


def evolve(state, rules, gens):
    head = state
    gen = 0
    totals = []
    while gen < gens:
        if head.p:
            head = LLNode(head.i - 2, False).add_right(LLNode(head.i - 1, False).add_right(head))

        current = head
        last = None
        total = 0
        pm2, pm1 = False, False
        while current is not None:
            pn = rules.get((pm2, pm1, current.p, right_or_false(current), right_or_false(current.right)), False)
            pm2, pm1 = pm1, current.p
            total += current.i if current.p else 0
            current.p = pn
            last = current
            current = current.right

        if last.p:
            last.add_right(LLNode(last.i + 1, False).add_right(LLNode(last.i + 2, False)))

        gen += 1
        totals.append(total)

    return head, totals


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        st_str = in_file.readline()[15:].rstrip()
        rules = dict([parse_rule(x) for x in in_file.readlines() if x != '\n'])

    new_state, _ = evolve(parse_state(st_str), rules, 20)
    print("Part 1: %d" % (count_pots(new_state),))
    _, totals = evolve(parse_state(st_str), rules, 1000)
    print("Part 2: %d" % (extrapolate_repeating(totals, 3, 50000000000),))


if __name__ == '__main__':
    main('12_input.txt')
