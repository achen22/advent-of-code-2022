from typing import Sequence

class Chamber:
    ROCKS = (
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 1))
    )

    def __init__(self, jets: str, width: int = 7, spawn: Sequence[int] = None):
        self.height = 0
        self.width = width
        if spawn is None:
            spawn = (2, 3)
        spawn = spawn[0] + width * spawn[1]

        self.filled = 0 # bits
        self.fallen = 0
        self.rocks = tuple(tuple(x + y * width + spawn for x, y in xy) for xy in Chamber.ROCKS)

        self.jetcount = len(jets)
        jets = ('0' if c == '<' else '1' for c in jets[::-1])
        self.jetbits = int("".join(jets), 2)
    
    def is_space(self, xy: int | Sequence[int]):
        if type(xy) != int:
            xy = xy[0] + xy[1] * self.width
        return self.filled & (1 << xy) == 0

    def next_jet(self):
        result = self.jetbits & 1
        self.jetbits += result << self.jetcount
        self.jetbits >>= 1
        return result

    def next_rock(self):
        rock = self.rocks[self.fallen % len(self.rocks)]
        self.fallen += 1
        rock = tuple(self.height * self.width + r for r in rock)
        while True:
            jet = self.next_jet()
            if all((r + jet) % self.width != 0 for r in rock):
                if jet == 0:
                    jet = -1
                step = tuple(r + jet for r in rock)
                if all(self.is_space(r) for r in step):
                    rock = step
            
            if rock[0] < self.width:
                break
            step = tuple(r - self.width for r in rock)
            if any(self.is_space(r) == False for r in step):
                break
            rock = step
        for r in rock:
            self.filled |= 1 << r
        height = r // self.width + 1
        if self.height <= height:
            self.height = height
    
    def ascii(self, height: int = 0):
        result = []
        if height != 0:
            height = max(0, self.height - height)
        for row in range(self.height - 1, height - 1, -1):
            row = range(row * self.width, (row + 1) * self.width)
            row = "".join("#."[self.is_space(i)] for i in row)
            result.append('|' + row + '|')
        if height == 0:
            result.append('+' + '-' * self.width + '+')
        return '\n'.join(result)

with open("input") as f:
    chamber = Chamber(f.read().rstrip())

for _ in range(2022):
    chamber.next_rock()
    #print(chamber.ascii())
print(chamber.height)
