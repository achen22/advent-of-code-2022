ROW = 2000000

def dist(a, b):
    return sum(abs(x2 - x1) for x1, x2 in zip(a, b))

sensors = {}
beacons = set()
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
        beacons.add(beacon)

ranges = []
for sensor, d in sensors.items():
    x, y = sensor
    d = d - abs(y - ROW)
    if d >= 0:
        ranges.append((x - d, x + d))

ranges.sort(key = lambda xy: xy[0])
merged = []
if ranges:
    merged.append(list(ranges[0]))
    for low, high in ranges[1:]:
        if low <= merged[-1][1]:
            merged[-1][1] = max(high, merged[-1][1])
        else:
            merged.append([low, high])

count = 0
beacons = sorted(x for x, y in beacons if y == ROW)
for low, high in merged:
    count += high + 1 - low
    while beacons and beacons[0] < low:
        beacons.pop(0)
    while beacons and beacons[0] <= high:
        beacons.pop(0)
        count -= 1
print(count)
