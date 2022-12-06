with open("input") as f:
    s = f.read(4)
    while len(set(s)) != 4:
        s = s[1:] + f.read(1)
    print(f.tell())
