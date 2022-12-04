score = 0

with open("input") as f:
    shared = None
    count = 0
    for line in f.readlines():
        line = line[:-1]
        if count == 0:
            shared = set(line)
        else:
            shared.intersection_update(line)
        if count == 2:
            assert len(shared) == 1
            count -= 3
            for l in shared:
                # add priority to score
                if l.isupper():
                    score += ord(l) - ord('A') + 27
                else:
                    score += ord(l) - ord('a') + 1
        count += 1

print(score)
