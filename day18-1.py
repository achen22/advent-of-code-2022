def surfaces(cube: tuple[int, int, int]):
    x, y, z = cube
    for i in (1, -1):
        yield (x, y, z + i)
        yield (x, y + i, z)
        yield (x + i, y, z)

cubes = set()
count = 0
with open("input") as f:
    for line in f.readlines():
        cube = tuple(int(s) for s in line.rstrip().split(','))
        cubes.add(cube)
        count += 6
        for c in surfaces(cube):
            if c in cubes:
                count -= 2

print(count)
