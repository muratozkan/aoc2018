LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Tree(object):

    def __init__(self, name, node_c, meta_c):
        self.name = name
        self.node_c = node_c
        self.meta_c = meta_c
        self.nodes = []
        self.metadata = []

    def __repr__(self):
        return '(%s: %2d %2d)' % (self.name, self.node_c, self.meta_c)

    def node_size(self):
        if self.node_c == 0:
            return 2 + self.meta_c

        node_sizes = [n.node_size() for n in self.nodes]
        return sum(node_sizes) + 2 + self.meta_c

    def meta_sum(self):
        return sum(self.metadata) + sum([n.meta_sum() for n in self.nodes])

    def value(self):
        if self.node_c == 0:
            return sum(self.metadata)

        val = 0
        for m in self.metadata:
            if m > self.node_c:
                continue
            else:
                val += self.nodes[m - 1].value()
        return val


def read_node(pos, ints, name_i):
    if pos + 1 > len(ints):
        return None

    node = Tree(LETTERS[name_i], ints[pos], ints[pos + 1])

    child_size = 0
    name_c = name_i
    for ni in range(node.node_c):
        name_c += 1
        child = read_node(pos + child_size + 2, ints, name_c)
        node.nodes.append(child)
        child_size += child.node_size()

    if node.meta_c > 0:
        meta_begin = pos + child_size + 2
        node.metadata = list(ints[meta_begin:meta_begin + node.meta_c])

    return node


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        line = in_file.readline()
        content = [int(x) for x in line.split(' ')]

    node = read_node(0, content, 0)

    print("Part 1: %d" % (node.meta_sum()))
    print("Part 2: %d" % (node.value()))


if __name__ == '__main__':
    main('8_input.txt')
