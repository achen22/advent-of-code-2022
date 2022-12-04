count = 0

def overlaps(a, b):
    if a[0] > b[0]:
        a, b = b, a
    return a[1] >= b[0]

with open("input") as f:
    for line in f.readlines():
        line = (s.split("-") for s in line[:-1].split(","))
        first, second = [[int(i), int(j)] for i, j in line]
        if overlaps(first, second):
            count += 1

print(count)
