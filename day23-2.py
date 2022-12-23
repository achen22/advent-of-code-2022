from collections import deque

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def display(elves):
    xrange, yrange = (range(min(x), max(x) + 1) for x in zip(*elves))
    for y in yrange:
        print("".join('#' if (x, y) in elves else '.' for x in xrange))
    print()

ADJACENT = ((0, -1), (-1, -1), (1, -1), (0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0))
proposals = deque((
    ((0, -1), (-1, -1), (1, -1)), # North
    ((0, 1), (-1, 1), (1, 1)),    # South
    ((-1, 0), (-1, -1), (-1, 1)), # West
    ((1, 0), (1, -1), (1, 1))     # East
))

elves = set()
with open("input") as f:
    y = 0
    for line in f.readlines():
        line = line.rstrip()
        for x in range(len(line)):
            if line[x] == '#':
                elves.add((x, y))
        y += 1

#display(elves)
steps = True
count = 0
while steps:
    steps = {}
    for xy in elves:
        if all(add(xy, p) not in elves for p in ADJACENT):
            continue
        step = None
        for proposal in proposals:
            if all(add(xy, p) not in elves for p in proposal):
                step = add(xy, proposal[0])
                break
        if step is None:
            continue
        if step not in steps:
            steps[step] = xy
        else:
            steps[step] = None
    for k, v in steps.items():
        if v is not None:
            elves.remove(v)
            elves.add(k)
    #display(elves)
    #print(len(steps), end='\r')
    proposals.rotate(-1)
    count += 1

print(count)
