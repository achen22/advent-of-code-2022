DIRECTION = ((1, 0), (0, 1), (-1, 0), (0, -1))

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

warp = [{}, {}, {}, {}]
for row in range(1, y):
    left, right = (f(i for i, j in grove.keys() if j == row) for f in (min, max))
    warp[0][(right, row)] = (left, row)
    warp[2][(left, row)] = (right, row)
x = max(i for i, _ in grove) + 1
for column in range(1, x):
    up, down = (f(j for i, j in grove.keys() if i == column) for f in (min, max))
    warp[1][(column, down)] = (column, up)
    warp[3][(column, up)] = (column, down)

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
                step = tuple(x + i for x, i in zip(xy, DIRECTION[facing]))
            if not grove[step]:
                break
            xy = step
            count -= 1

print(1000 * xy[1] + 4 * xy[0] + facing)
