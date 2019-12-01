class TNode(object):

    def __init__(self):
        self.ds = []  # directions for current node
        self.parent = None
        self.nodes = []  # child nodes

    def add_child(self, node):
        self.nodes.append(node)
        node.parent = self

    def __repr__(self):
        return 'Node [%s]' % (','.join(self.ds),)


def exp_tree(rgx):
    rgx = rgx[1:-1]
    head = TNode()
    visit_stack = []
    current = head
    for c in rgx:
        if c == '(':
            # add a branch to current node
            node = TNode()
            current.add_child(node)
            visit_stack.insert(0, current)
            current = node
        elif c == '|':
            current = visit_stack.pop(0)
            # add another branch to parent node
            node = TNode()
            current.add_child(node)
            visit_stack.insert(0, current)
            current = node
        elif c == ')':
            current = visit_stack.pop(0)
            # go process parent
        else:
            current.ds.append(c)
    return head


def farthest_room_dist(tree):
    node_dst = {}

    node_stack = [tree]
    while len(node_stack) > 0:
        current = node_stack.pop(0)

        parent_dst = node_dst.get(current.parent) if current.parent else 0
        current_dst = parent_dst + len(current.ds)
        node_dst[current] = current_dst

        for nodes in current.nodes:
            node_stack.append(nodes)

    return max(node_dst.values())


def main(in_str):
    with open(in_str, 'r') as in_file:
        rgx = list(in_file.readline().rstrip('\n'))

    tree = exp_tree(rgx)
    dst = farthest_room_dist(tree)
    print('Part 1: %d' % (dst,))


if __name__ == '__main__':
    main('20_input.txt')
