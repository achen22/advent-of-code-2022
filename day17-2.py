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
        self.maxdrop = 0
        self.skip: dict[str, int] = {}

        self.width = width
        self.render = (1 << (self.maxdrop + 20) * self.width) - 1
        self.filled = (1 << width) - 1 # bits
        self.count = 0
        if spawn is None:
            spawn = (2, 3)
        spawn = spawn[0] - width * (spawn[1] + 1)
        self.rocks = tuple(tuple(x - y * width + spawn for x, y in xy) for xy in Chamber.ROCKS)

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
        rock = self.rocks[self.count % len(self.rocks)]
        self.count += 1
        while True:
            jet = self.next_jet()
            if all((r + jet) % self.width != 0 for r in rock):
                if jet == 0:
                    jet = -1
                step = tuple(r + jet for r in rock)
                if all(r < 0 or self.is_space(r) for r in step):
                    rock = step
            
            step = tuple(r + self.width for r in rock)
            if any(r >= 0 and not self.is_space(r) for r in step):
                break
            rock = step

        diff = rock[-1] // self.width
        if diff < 0:
            self.height -= diff
            diff = self.width * -diff
            rock = tuple(r + diff for r in rock)
            self.filled <<= diff
            self.filled &= self.render
        elif self.maxdrop < diff:
            #print(diff)
            self.maxdrop = diff
            self.render = (1 << (diff + 20) * self.width) - 1

        for r in rock:
            self.filled |= 1 << r
    
    def drop_rocks(self, n: int = 1):
        if not self.skip:
            states = []
            for _ in range(len(self.rocks)):
                states.append({})

            state: dict = states[0]
            while self.filled not in state:
                state[self.filled] = (self.count, self.height)
                self.next_rock()
                n -= 1
                if n == 0:
                    return
                states = states[1:] + [state]
                state = states[0]
            count, height = state[self.filled]
            self.skip = {
                "rock": self.count % len(self.rocks),
                "count": self.count - count,
                "height": self.height - height
            }
        
        while self.count % len(self.rocks) != self.skip["rock"]:
            self.next_rock()
            n -= 1
            if n == 0:
                return
        
        skip = self.skip["count"]
        if n >= skip:
            skip = n // skip
            self.height += skip * self.skip["height"]
            skip *= self.skip["count"]
            self.count += skip
            n -= skip
        
        for _ in range(n):
            self.next_rock()

    def ascii(self, height: int = 4):
        result = []
        for row in range(self.maxdrop + height):
            row = range(row * self.width, (row + 1) * self.width)
            row = "".join("#."[self.is_space(i)] for i in row)
            result.append('|' + row + '|')
        result[0] += f" {self.height}"
        return '\n'.join(result)

with open("input") as f:
    chamber = Chamber(f.read().rstrip())

#for _ in range(2022):
    #chamber.next_rock()
    #print(chamber.ascii())
    #print()
chamber.drop_rocks(1000000000000)
print(chamber.height)
