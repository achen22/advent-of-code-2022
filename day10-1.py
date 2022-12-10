watchlist = [20, 60, 100, 140, 180, 220]
values = []

with open("input") as f:
    cycle = 1
    x = 1
    for line in f.readlines():
        line = line.rstrip()
        cycle += 1
        if cycle >= watchlist[0]:
            values.append(x * watchlist.pop(0))
            if len(watchlist) == 0:
                break
        if line == "noop":
            continue
        # line[:4] == "addx"
        cycle += 1
        x += int(line[5:])

print(sum(values))
