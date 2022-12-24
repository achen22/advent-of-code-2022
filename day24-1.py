def display(valley, width):
    for i in range(len(valley)):
        if i % width == 0:
            print()
        tile = valley[i]
        if len(tile) == 0:
            print('.', end="")
        elif len(tile) == 1:
            print(tile[0], end="")
        else:
            print(len(tile), end="")
    print()

def move(valley, width, i):
    moves = [i]
    if i % width != 0:
        moves.append(i - 1)
    if i % width != width - 1:
        moves.append(i + 1)
    if i >= width:
        moves.append(i - width)
    if i < len(valley) - width:
        moves.append(i + width)
    return moves

with open("input") as f:
    line = f.readline()
    assert line[:3] == "#.#"
    width = len(line.rstrip()) - 2
    valley = []
    for line in f.readlines():
        assert line[0] == '#'
        if line[1] == '#':
            break
        for c in line[1:]:
            if c == '#':
                break
            valley.append([] if c == '.' else [c])
    end = len(valley) - width + line.index('.') - 1

blizzard = {
    '^': lambda x: (x - width) % len(valley),
    'v': lambda x: (x + width) % len(valley),
    '<': lambda x: x // width * width + (x - 1) % width,
    '>': lambda x: x // width * width + (x + 1) % width
}

#display(valley, width)
count = 0
while valley[end] != ["E"]:
    step = {'^': [], 'v': [], '<': [], '>': [], 'E': []}
    for i in range(len(valley)):
        tile = valley[i]
        for c in tile:
            if c == 'E':
                step['E'].extend(move(valley, width, i))
            else:
                step[c].append(blizzard[c](i))
        tile.clear()
    for c in blizzard.keys():
        for i in step[c]:
            valley[i].append(c)
    step = set(step['E'])
    for i in step:
        if len(valley[i]) == 0:
            valley[i].append('E')
    if len(valley[0]) == 0:
        valley[0].append('E')
    #display(valley, width)
    count += 1

print(count + 1)
