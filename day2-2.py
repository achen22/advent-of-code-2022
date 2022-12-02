score = 0

with open("input") as f:
    for line in f.readlines():
        opponent = ord(line[0])
        winlose = ord(line[2]) - ord('Y')
        player = (opponent - ord('A') + winlose) % 3 + ord('X')
        score += player - ord('X') + 1
        diff = player - opponent
        score += (diff - 1) % 3 * 3

print(score)
