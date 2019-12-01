from blist import blist


def max_score(player_c, max_s):
    circle = blist()
    circle.append(0)
    current_i = 0
    m = 0
    scores = [0] * player_c
    player = 0
    while m < max_s + 1:
        m += 1
        if m % 23 == 0:
            next_i = (current_i - 7) % len(circle)
            scores[player] += m + circle[next_i]
            del circle[next_i]
        else:
            next_i = (current_i + 1) % len(circle) + 1
            circle.insert(next_i, m)
        current_i = next_i
        player = (player + 1) % player_c
        if m % 10000 == 0:
            print('.', end='')

    return max(scores)


def main():
    # print("Part 1: %s" % (max_score(10, 1618)))
    # print("Part 1: %s" % (max_score(447, 71510)))
    print("Part 2: %s" % (max_score(447, 7151000)))


if __name__ == '__main__':
    main()
