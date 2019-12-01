class Node(object):

    def __init__(self, val):
        self.val = val
        self.nodes = []
        self.prevs = []

    def search_df(self, val):
        if self.val == val:
            return None, self

        for n in self.nodes:
            prev, found = n.search_df(val)
            if found:
                prev = prev if prev else self
                return prev, found

        return None, None

    def add_edge(self, other):
        self.nodes.append(other)
        other.prevs.append(self)

    def __repr__(self):
        return '(%s)' % self.val

    def __eq__(self, other):
        return other is Node and self.val == other.val

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.val)


def parse(line):
    return line[5], line[36]


def debug_print_traverse(n, queue, unavailable):
    queue_str = ''.join([x.val for x in queue])
    unavailable_str = ''.join([x.val for x in unavailable])
    print('Current: [%s] Queue: [%s] Unavailable: [%s]' % (n.val, queue_str, unavailable_str))


def next_dfs(start):
    visited = set()
    unavailable = set()
    queued = set()
    n = start
    queue = []
    while True:
        visited.add(n.val)

        to_check = n.nodes + list(unavailable)
        for nc in to_check:
            if nc.val not in queued:
                if all([p.val in visited for p in nc.prevs]):
                    queue.insert(0, nc)
                    queued.add(nc.val)
                    if nc in unavailable:
                        unavailable.remove(nc)
                else:
                    unavailable.add(nc)

        if not queue:
            break

        queue = sorted(queue, key=lambda x: x.val)
        debug_print_traverse(n, queue, unavailable)
        n = queue.pop(0)
        yield n


def next_bfs(start):
    visited = set()
    unavailable = set()
    queued = set()
    n = start
    queue = []
    while True:
        visited.add(n.val)

        to_check = n.nodes + list(unavailable)
        for nc in to_check:
            if nc.val not in queued:
                if all([p.val in visited for p in nc.prevs]):
                    queue.append(nc)
                    queued.add(nc.val)
                    if nc in unavailable:
                        unavailable.remove(nc)
                else:
                    unavailable.add(nc)

        if not queue:
            break

        debug_print_traverse(n, queue, unavailable)
        n = queue.pop(0)
        yield n


def traverse(start):
    ls = []
    for node in next_dfs(start):
        ls.append(node.val)
    return ls


def build_graph(dep_s):
    nodes = {}
    for bef, aft in dep_s:
        n_bef = nodes.get(bef, Node(bef))
        nodes[bef] = n_bef

        n_aft = nodes.get(aft, Node(aft))
        nodes[aft] = n_aft

        n_bef.add_edge(n_aft)

    head, tail = Node('.'), Node('.')
    for _, node in nodes.items():
        if not len(node.prevs):
            head.add_edge(node)

        if not len(node.nodes):
            node.add_edge(tail)

    return nodes, head


def debug_print_time(sec, ws, processed):
    ws_str = '\t'.join(['%s (%3d)' % w for w in ws])
    p_str = ','.join(processed)
    print('%4d W: [%s] P: [%s]' % (sec, ws_str, p_str))


def time_taken(start, worker_c, time_func):
    next_node_fn = next_bfs(start)
    ws = [(None, 0)] * worker_c
    sec = 0
    processed = set('.')
    temps = []
    while True:
        for i in range(worker_c):
            v, t = ws[i]
            if t > 0:
                ws[i] = v, t - 1

            v, t = ws[i]
            if t == 0 and v is not None:
                processed.add(v)
                ws[i] = None, 0

            v, t = ws[i]
            if v is None:
                node = None
                for ti in range(len(temps)):
                    if all([p.val in processed for p in temps[ti].prevs]):
                        node = temps.pop(ti)
                        break

                if node is None:
                    node = next(next_node_fn, None)

                if node is None or node.val == '.':
                    continue
                if all([p.val in processed for p in node.prevs]):
                    ws[i] = node.val, time_func(node.val)
                else:
                    temps.append(node)

        if all([t == 0 for _, t in ws]):
            break

        debug_print_time(sec, ws, processed)
        sec += 1

    return sec


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [parse(x) for x in in_file.readlines()]

    nodes, head = build_graph(content)
    order = traverse(head)

    print('Part 1: %s' % (''.join(order).replace('.', ''),))

    # total = time_taken(head, 2, lambda x: ord(x) - ord('A') + 1)
    total = time_taken(head, 5, lambda x: ord(x) - ord('A') + 61)
    print('Part 2: %s' % (total,))


if __name__ == '__main__':
    main('7_input.txt')
