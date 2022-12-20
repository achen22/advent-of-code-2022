from collections import deque

with open("input") as f:
    original = tuple(int(line.rstrip()) * 811589153 for line in f.readlines())

size = len(original)
mixed = deque(range(size))
for _ in range(10):
    for i in range(size):
        #print(tuple(original[j] for j in mixed))
        n = original[i]
        if n == 0:
            continue
        n = mixed.index(i)
        mixed.rotate(-n)
        assert i == mixed.popleft()
        n = original[i]
        n %= size - 1
        mixed.insert(n, i)
    #print(tuple(original[j] for j in mixed))
mixed = tuple(original[j] for j in mixed)
offset = mixed.index(0)
print(sum(mixed[(i + offset) % size]for i in (1000, 2000, 3000)))
