score = 0

with open("input") as f:
    for line in f.readlines():
        line = line[:-1]
        half = len(line) // 2
        first = set(line[:half])
        second = set(line[half:])
        shared = first.intersection(second)
        for l in shared:
            # add priority to score
            if l.isupper():
                score += ord(l) - ord('A') + 27
            else:
                score += ord(l) - ord('a') + 1

print(score)
