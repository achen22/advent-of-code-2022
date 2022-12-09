knots = []
for _ in range(10):
    knots.append([0, 0])

tailset = set()
tailset.add((0, 0))

def update_head_pos(direction):
    assert direction in ('U', 'D', 'L', 'R')
    if direction == 'U':
        knots[0][1] += 1
    elif direction == 'D':
        knots[0][1] -= 1
    elif direction == 'L':
        knots[0][0] -= 1
    else: # direction == 'R'
        knots[0][0] += 1
    update_tail_pos()

def update_tail_pos(pos = 0):
    xdiff = knots[pos][0] - knots[pos + 1][0]
    ydiff = knots[pos][1] - knots[pos + 1][1]
    if abs(xdiff) <= 1 and abs(ydiff) <= 1:
        return
    if xdiff != 0:
        knots[pos + 1][0] += xdiff // abs(xdiff)
    if ydiff != 0:
        knots[pos + 1][1] += ydiff // abs(ydiff)
    if pos == len(knots) - 2:
        tailset.add(tuple(knots[pos + 1]))
    else:
        update_tail_pos(pos + 1)

with open("input") as f:
    for line in f.readlines():
        line = line.rstrip()
        if len(line) == 0:
            break
        line = line.split(' ')
        for _ in range(int(line[1])):
            update_head_pos(line[0])

print(len(tailset))
