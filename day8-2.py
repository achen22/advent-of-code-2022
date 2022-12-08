def scenic_score(trees, x, y):
    xlen = len(trees[0])
    ylen = len(trees)
    if x == 0 or y == 0 or x + 1 == xlen or y + 1 == ylen:
        return 0
    
    tree = trees[y][x]

    score = view_count(trees[y][x-1::-1], tree)   # left
    score *= view_count(trees[y][x+1:xlen], tree) # right

    column = tuple(trees[i][x] for i in range(len(trees)))
    score *= view_count(column[y-1::-1], tree)  # up
    score *= view_count(column[y+1:ylen], tree) # down

    return score

def view_count(view, height):
    count = 0
    while count < len(view) and view[count] < height:
        count += 1
    return min(count + 1, len(view))

trees = []
with open("input") as f:
    for line in f.readlines():
        trees.append(tuple(int(s) for s in line[:-1]))

max_score = 0
for j in range(1, len(trees) - 1):
    max_score = max(max_score, max(scenic_score(trees, i, j) for i in range(1, len(trees[j]) - 1)))

print(max_score)
