class NestedIntList(list):
    def parse(s):
        if type(s) == str:
            s = eval(s)
        result = s[:]
        for i in range(len(s)):
            if type(s[i]) != int:
                result[i] = NestedIntList.parse(s[i])
        return NestedIntList(result)
    
    def __lt__(self, other) -> bool:
        if type(other) == int:
            return self.__lt__(NestedIntList([other]))
        for a, b in zip(self, other):
            if type(a) == int and type(b) != int:
                a = NestedIntList([a])
            elif type(b) == int and type(a) != int:
                b = NestedIntList([b])
            if a == b:
                continue
            return a < b
        return len(self) < len(other)
    
    def __eq__(self, other) -> bool:
        if type(other) == int:
            other = NestedIntList([other])
        return super().__eq__(other)

pairs = []
with open("input") as f:
    line_count = 0
    for line in f.readlines():
        if line_count == 2:
            assert line.isspace()
            line_count = 0
            continue
        if line_count == 0:
            pairs.append([])
        pairs[-1].append(NestedIntList.parse(line.rstrip()))
        line_count += 1

total = 0
for i in range(len(pairs)):
    a, b = pairs[i]
    assert a != b
    if a < b:
        total += i + 1
print(total)
