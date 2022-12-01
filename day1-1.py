elves = []
with open("input") as f:
    calories = 0
    for line in f.readlines():
        line = line.strip()
        if line:
            calories += int(line)
        else:
            elves.append(calories)
            calories = 0
    elves.append(calories)
print(max(elves))
