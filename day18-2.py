def surfaces(cube: tuple[int, int, int]):
    x, y, z = cube
    for i in (1, -1):
        yield (x, y, z + i)
        yield (x, y + i, z)
        yield (x + i, y, z)

grid = {}
with open("input") as f:
    for line in f.readlines():
        cube = tuple(int(s) for s in line.rstrip().split(','))
        grid[cube] = 0
        for c in surfaces(cube):
            if c not in grid:
                grid[c] = 1
            elif grid[c] != 0:
                grid[c] += 1

cubes = set(c for c, n in grid.items() if n == 0)
bounds = tuple((min(x), max(x)) for x in zip(*grid.keys()))
start, end = zip(*bounds)
external = set([start])
edge = set([start])
while edge:
    prev = edge
    edge = set()
    for cube in prev:
        for s in surfaces(cube):
            if s in cubes or s in external:
                continue
            if any(x < b[0] or x > b[1] for x, b in zip(s, bounds)):
                continue
            edge.add(s)
            external.add(s)

print(sum(v for k, v in grid.items() if k in external))
