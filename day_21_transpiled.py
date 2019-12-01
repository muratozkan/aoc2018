r0, r1, r2, r3, r4 = 0, 0, 0, 0, 0

seen = set()
last = 0

r2 = 0
r1 = r2 | 65536
r2 = 1250634
while True:
    r4 = r1 & 255
    r2 = r4 + r2
    r2 = ((r2 & 0xFFFFFF) * 65899) & 0xFFFFFF
    r4 = 1 if 256 > r1 else 0
    if r4 == 1:
        # print('%d %d %d %d %d' % (r0, r1, r2, r3, r4))
        if r2 in seen:
            print('Found: %d' % last)
            exit(0)
        else:
            seen.add(r2)
            last = r2

        r1 = r2 | 65536
        r2 = 1250634
        continue

    r4 = 0
    while True:
        r3 = r4 + 1
        r3 = r3 * 256
        r3 = 1 if r3 > r1 else 0
        if r3 == 1:
            break

        r4 = r4 + 1

    r1 = r4

