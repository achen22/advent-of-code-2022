from math import gcd
from itertools import product, chain

DIRECTION = ((1, 0), (0, 1), (-1, 0), (0, -1))

def rotate(edge: int, xy: tuple[int, int], n: int = 1):
    n %= len(DIRECTION)
    x, y = xy
    while n > 0:
        x, y = edge - y - 1, x
        n -= 1
    return (x, y)

grove = {}
steps = []
with open("input") as f:
    y = 1
    line = f.readline().rstrip()
    while line:
        for i in range(len(line)):
            if line[i] == ' ':
                continue
            grove[(i + 1, y)] = line[i] == '.'
        y += 1
        line = f.readline().rstrip()
    line = f.readline()
    token = line[0]
    isdigit = token.isdigit()
    for c in line[1:]:
        if c.isdigit() == isdigit:
            token += c
        else:
            if isdigit:
                token = int(token)
            steps.append(token)
            token = c
            isdigit = not isdigit

edge = y - 1
for row in range(1, y):
    left, right = (f(i for i, j in grove.keys() if j == row) for f in (min, max))
    edge = gcd(edge, left - 1, right)
x = max(i for i, _ in grove) + 1
for column in range(1, x):
    up, down = (f(j for i, j in grove.keys() if i == column) for f in (min, max))
    edge = gcd(edge, up - 1, down)

bounds = (x // edge, y // edge)
net = {(i, j): [None, None, None, None] for i, j in product(*(range(b) for b in bounds)) if (i * edge + 1, j * edge + 1) in grove}
for c in net.keys():
    for n in range(len(DIRECTION)):
        d = tuple(sum(x) for x in zip(c, DIRECTION[n]))
        if d in net:
            net[c][n] = (d, n)
while any(v == None for v in chain.from_iterable(net.values())):
    pass
    for c in net.keys():
        for n in range(len(DIRECTION)):
            down = (n + 1) % len(DIRECTION)
            if net[c][down] != None:
                continue
            east = net[c][n]
            if east == None:
                continue
            east, n = east
            south = net[east][(n + 1) % len(DIRECTION)]
            if south == None:
                continue
            south, n = south
            net[c][down] = (south, (n - 1) % len(DIRECTION))

warp = [{}, {}, {}, {}]
for c in net.keys():
    for n in range(len(DIRECTION)):
        d = tuple(sum(x) for x in zip(c, DIRECTION[n]))
        if d in net:
            continue
        source = tuple((edge - 1, i) for i in range(edge))
        source = tuple(rotate(edge, xy, n) for xy in source)
        source = tuple(tuple(x * edge + 1 + i for x, i in zip(c, xy)) for xy in source)

        warp_dir = warp[n]
        d, n = net[c][n]
        dest = tuple((0, i) for i in range(edge))
        dest = tuple(rotate(edge, xy, n) for xy in dest)
        dest = tuple(tuple(x * edge + 1 + i for x, i in zip(d, xy)) for xy in dest)

        for s, d in zip(source, dest):
            warp_dir[s] = (d, n)

x = min(i for i, j in grove if j == 1)
xy = (x, 1)
facing = 0
for step in steps:
    if step == "L":
        facing -= 1
        facing %= len(DIRECTION)
    elif step == "R":
        facing += 1
        facing %= len(DIRECTION)
    else:
        #print(xy, ">v<^"[facing])
        assert type(step) == int
        count = step
        while count > 0:
            if xy in warp[facing]:
                step = warp[facing][xy]
            else:
                step = (tuple(x + i for x, i in zip(xy, DIRECTION[facing])), facing)
            if not grove[step[0]]:
                break
            xy, facing = step
            count -= 1

print(1000 * xy[1] + 4 * xy[0] + facing)
