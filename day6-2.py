with open("input") as f:
    s = f.read(14)
    while len(set(s)) != 14:
        s = s[1:] + f.read(1)
    print(f.tell())
