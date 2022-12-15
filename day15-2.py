from itertools import combinations, product

XYMAX = 4000000

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.m = (y2 - y1) // (x2 - x1)
        self.c = (x2 * y1 - x1 * y2) // (x2 - x1)
        self.dom = tuple(f(x1, x2) for f in (min, max))
        self.ran = tuple(f(y1, y2) for f in (min, max))
    
    def intersect(self, other):
        if type(other) != Line:
            return
        if len(merge((self.dom, other.dom))) != 1:
            return
        if len(merge((self.ran, other.ran))) != 1:
            return
        if self.m == other.m:
            return
        x = other.c - self.c
        if x % 2 != 0:
            return
        x //= self.m - other.m
        y = self.m * x + self.c
        return (x, y)

def dist(a, b):
    return sum(abs(x2 - x1) for x1, x2 in zip(a, b))

def merge(l, merge_adjacent = False):
    if not l:
        return []
    l = sorted(l, key = lambda e: e[0])
    result = [list(l[0])]
    for low, high in l[1:]:
        if low <= result[-1][1] + merge_adjacent:
            result[-1][1] = max(high, result[-1][1])
        else:
            result.append([low, high])
    return result

sensors = {}
with open("input") as f:
    for line in f.readlines():
        line = line.rstrip().split(' ')
        assert line[2][:2] == "x="
        sx = int(line[2][2:-1])
        assert line[3][:2] == "y="
        sy = int(line[3][2:-1])
        assert line[8][:2] == "x="
        bx = int(line[8][2:-1])
        assert line[9][:2] == "y="
        by = int(line[9][2:])
        sensor = (sx, sy)
        beacon = (bx, by)
        sensors[sensor] = dist(sensor, beacon)

bounds = []
for xy, d in sensors.items():
    x, y = xy
    d += 1
    corners = []
    for s in (-1, 1):
        corners.append((x, y + s * d))
        corners.append((x + s * d, y))
    lines = []
    for a, b in combinations(corners, 2):
        if a[0] == b[0] or a[1] == b[1]:
            continue
        lines.append(Line(*a, *b))
    bounds.append(lines)

intersects = {}
for lines1, lines2 in combinations(bounds, 2):
    for line1, line2 in product(lines1, lines2):
        xy = line1.intersect(line2)
        if not xy:
            continue
        if any(c < 0 or c >= XYMAX for c in xy):
            continue
        if xy in intersects:
            intersects[xy] += 1
        else:
            intersects[xy] = 1

for xy, n in intersects.items():
    if n >= 4:
        found = None
        for sensor, d in sensors.items():
            if dist(xy, sensor) <= d:
                found = sensor
                break
        if not found:
            break

x, y = xy
print(x * 4000000 + y)
