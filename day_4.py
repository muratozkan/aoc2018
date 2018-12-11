
def parse(in_str):
    # [1518-11-01 00:00]
    ti = int(in_str[6:17].replace('-', '').replace(':', '').replace(' ', ''))
    dt = in_str[6:11]

    g, w = None, None
    if in_str[19] == 'G':  # Guard #10 begins shift
        gi = in_str[25:].find(' ')
        g = int(in_str[26:25 + gi])
    elif in_str[19] == 'w':
        w = True
    elif in_str[19] == 'f':
        w = False

    m = None
    if w is not None:
        m = int(in_str[15:17])

    return ti, (dt, m), g, w


def day_guard_times(time_log):
    dg_t = {}
    last_g = None
    for _, (dt, m), g, w in time_log:
        actual_g = g if g else last_g
        last_g = actual_g

        if w is not None:
            gt_pair = dg_t.get(dt, (actual_g, []))
            gt_pair[1].append((m, w))
            dg_t[dt] = gt_pair

    return dg_t


def sleep_time(ms):
    # [(23, false), (32, true)]
    s_tot = 0
    s_cur = 0
    for m, w in ms:
        if w:
            s_tot += m - s_cur
            s_cur = 0
        else:
            s_cur = m
    return s_tot


def sleep_mins(ms):
    ls = []
    s_cur = 0
    for m, w in ms:
        if w:
            ls = ls + [i for i in range(s_cur, m)]
            s_cur = 0
        else:
            s_cur = m
    return ls


def guard_asleep(days, dg_t):
    g_s = {}
    for d in days:
        gp = dg_t.get(d, None)
        if not gp:
            continue

        g, ms = gp
        g_dt_ms = g_s.get(g, [])
        g_dt_ms.append((d, ms))
        g_s[g] = g_dt_ms

    return g_s


def most_asleep_guard(g_s):
    a_gs = []
    for g, g_dt_ms in g_s.items():
        g_dts = map(lambda x: (x[0], sleep_time(x[1])), g_dt_ms)
        tot_sleep = sum(map(lambda x: x[1], g_dts))
        a_gs.append((g, tot_sleep))
    return max(a_gs, key=lambda x: x[1])


def asleep_minute(g, g_s):
    ds = g_s.get(g)

    mins = {}
    for i in range(60):
        mins[i] = 0

    for (d, ms) in ds:
        s_cur = 0
        for m, w in ms:
            if w:
                for i in range(s_cur, m):
                    mins[i] += 1
                s_cur = 0
            else:
                s_cur = m

    return mins


def debug_print(days, dg_t):
    for d in days:
        p = dg_t.get(d)
        if not p:
            continue
        g, ms = p
        ls = sleep_mins(ms)
        s_l = set(ls)
        print("%s\t%04d\t:%s" % (d, g, ''.join(['#' if x in s_l else '.' for x in range(60)])))


def main(in_txt):
    with open(in_txt, 'r') as in_file:
        content = [parse(x) for x in in_file.readlines()]

    content.sort(key=lambda x: x[0])
    dg_t = day_guard_times(content)
    days = list(dg_t.keys())

    debug_print(days, dg_t)

    g_s = guard_asleep(days, dg_t)

    mag, mins = most_asleep_guard(g_s)
    mins = asleep_minute(mag, g_s)

    m = max(list(mins.items()), key=lambda x: x[1])[0]

    print("Part 1: %s" % (mag * m))

    g_mm = []
    for g in g_s.keys():
        mns = asleep_minute(g, g_s)
        mnt, c = max(list(mns.items()), key=lambda x: x[1])
        g_mm.append((g, mnt, c))

    g_mm_max = max(g_mm, key=lambda x: x[2])
    print("Part 2: %s" % (g_mm_max[0] * g_mm_max[1]))


if __name__ == '__main__':
    main('4_input.txt')
