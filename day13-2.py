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

dividers = tuple(NestedIntList.parse([[i]]) for i in (2, 6))
packets = []
packets.extend(dividers)
with open("input") as f:
    for line in f.readlines():
        if line.isspace():
            continue
        packets.append(NestedIntList.parse(line.rstrip()))

packets.sort()
indices = tuple(packets.index(p) + 1 for p in dividers)
print(indices[0] * indices[1])
