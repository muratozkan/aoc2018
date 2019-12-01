POS_L = ['^', '>', 'v', '<']

POS_I = {'^': 0, '>': 1, 'v': 2, '<': 3}

POS_V = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}


class Cart(object):

    def __init__(self, i, pos, h):
        self.i = i
        self.pos = pos
        self.h = h  # heading

    def __lt__(self, other):
        ox, oy = other.pos
        sx, sy = self.pos
        if sy == oy:
            return sx < ox

        return sy < oy

    def next_pos(self):
        dir_v = POS_V[self.h]
        return self.pos[0] + dir_v[0], self.pos[1] + dir_v[1]

    def __repr__(self):
        return '[%d @ %d,%d]' % (self.i, self.pos[0], self.pos[1])


def find_carts(cmap):
    carts = []
    for y in range(len(cmap)):
        for x in range(len(cmap[0])):
            c = cmap[y][x]
            cart = None
            if c == 'v' or c == '^':
                cart = Cart(len(carts) + 1, (x, y), c)
                cmap[y][x] = '|'
            elif c == '>' or c == '<':
                cart = Cart(len(carts) + 1, (x, y), c)
                cmap[y][x] = '-'

            if cart:
                carts.append(cart)

    return carts


NEXT_HEADING = {
    ('^', '\\'): '<',
    ('>', '\\'): 'v',
    ('<', '\\'): '^',
    ('v', '\\'): '>',
    ('^', '/'): '>',
    ('>', '/'): '^',
    ('v', '/'): '<',
    ('<', '/'): 'v'
}


def simulate_crash(cmap, carts):
    crash_pos = None
    tick = 0
    cart_xing = {}
    while True:
        carts.sort()
        for cart in carts:
            new_x, new_y = cart.next_pos()
            new_c = cmap[new_y][new_x]
            new_heading = cart.h
            if new_c == '\\' or new_c == '/':
                new_heading = NEXT_HEADING[(cart.h, new_c)]
            elif new_c == '+':
                turn_dir = cart_xing.get(cart.i, -1)
                new_heading = POS_L[(POS_I[cart.h] + turn_dir) % 4]
                cart_xing[cart.i] = (turn_dir + 2) % 3 - 1

            cart.h = new_heading
            cart.pos = new_x, new_y

            cart_pos = set([c.pos for c in carts if c.i != cart.i])
            if (new_x, new_y) in cart_pos:
                crash_pos = new_x, new_y

            if crash_pos is not None:
                break

        if crash_pos is not None:
            break

        tick += 1

    return crash_pos


def simulate_last(cmap, carts):
    tick = 0
    cart_xing = {}
    while True:
        carts.sort()
        for cart in carts:
            if cart.i == 0:
                continue

            new_x, new_y = cart.next_pos()
            new_c = cmap[new_y][new_x]
            new_heading = cart.h
            if new_c == '\\' or new_c == '/':
                new_heading = NEXT_HEADING[(cart.h, new_c)]
            elif new_c == '+':
                turn_dir = cart_xing.get(cart.i, -1)
                new_heading = POS_L[(POS_I[cart.h] + turn_dir) % 4]
                cart_xing[cart.i] = (turn_dir + 2) % 3 - 1

            cart.h = new_heading
            cart.pos = new_x, new_y

            cart_pos = set([c.pos for c in carts if c.i != cart.i])
            if (new_x, new_y) in cart_pos:
                for cr in filter(lambda c: c.pos == cart.pos, carts):
                    cr.i = 0

        carts = [c for c in carts if c.i != 0]

        if len(carts) == 1:
            break

        tick += 1

    return carts[0]


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        cmap = [list(y.rstrip('\n')) for y in in_file.readlines()]

    print('Part 1: %s' % (simulate_crash(cmap, find_carts(cmap)),))
    print('Part 2: %s' % (simulate_last(cmap, find_carts(cmap)),))


if __name__ == '__main__':
    main('13_input.txt')
