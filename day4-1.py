count = 0

def contains(a, b):
    return a[0] >= b[0] and a[1] <= b[1]

with open("input") as f:
    for line in f.readlines():
        line = (s.split("-") for s in line[:-1].split(","))
        first, second = [[int(i), int(j)] for i, j in line]
        if contains(first, second) or contains(second, first):
            count += 1

print(count)
