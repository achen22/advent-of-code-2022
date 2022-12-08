def transpose(arr):
    return [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]

def get_visibility(trees):
    visibility = [0 for _ in trees]
    for _ in range(2):
        tallest = -1
        i = 0
        while i < len(trees):
            visibility[i] |= trees[i] > tallest
            tallest = max(trees[i], tallest)
            i += 1
        visibility = visibility[::-1]
        trees = trees[::-1]
    return visibility

trees = []
with open("input") as f:
    for line in f.readlines():
        trees.append(tuple(int(s) for s in line[:-1]))

vis_row = [get_visibility(row) for row in trees]
vis_col = transpose([get_visibility(col) for col in transpose(trees)])

print(sum(sum(a | b for a, b in zip(v1, v2)) for v1, v2 in zip(vis_row, vis_col)))
