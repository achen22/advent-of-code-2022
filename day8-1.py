def is_visible(trees, x, y):
    xlen = len(trees[0])
    ylen = len(trees)
    tree = trees[y][x]
    if x == 0 or y == 0 or x + 1 == xlen or y + 1 == ylen:
        return True
    if all(trees[y][i] < tree for i in range(x)):
        return True
    if all(trees[y][i] < tree for i in range(x + 1, xlen)):
        return True
    if all(trees[i][x] < tree for i in range(y)):
        return True
    return all(trees[i][x] < tree for i in range(y + 1, ylen))

trees = []
with open("input") as f:
    for line in f.readlines():
        trees.append(tuple(int(s) for s in line[:-1]))

visible = sum(is_visible(trees, i, j) for j in range(len(trees)) for i in range(len(trees[0])))

print(visible)
