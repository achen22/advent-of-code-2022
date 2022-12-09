head = [0, 0]
tail = [0, 0]
tailset = set()
tailset.add((0, 0))

def update_head_pos(direction):
    assert direction in ('U', 'D', 'L', 'R')
    if direction == 'U':
        head[1] += 1
    elif direction == 'D':
        head[1] -= 1
    elif direction == 'L':
        head[0] -= 1
    else: # direction == 'R'
        head[0] += 1

def update_tail_pos():
    xdiff = head[0] - tail[0]
    ydiff = head[1] - tail[1]
    if abs(xdiff) <= 1 and abs(ydiff) <= 1:
        return
    if xdiff != 0:
        tail[0] += xdiff // abs(xdiff)
    if ydiff != 0:
        tail[1] += ydiff // abs(ydiff)
    tailset.add(tuple(tail))

with open("input") as f:
    for line in f.readlines():
        line = line.rstrip()
        if len(line) == 0:
            break
        line = line.split(' ')
        for _ in range(int(line[1])):
            update_head_pos(line[0])
            update_tail_pos()

print(len(tailset))
