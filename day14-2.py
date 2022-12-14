class Cave(set):
    def __init__(self):
        self.source = (500, 0)
        self.depth = 0
        self.x_min = 500
        self.x_max = 500
        super(Cave, self).__init__()
    
    def add_path(self, path):
        self.x_min = min(self.x_min, *(x for x, _ in path))
        self.x_max = max(self.x_max, *(x for x, _ in path))
        self.depth = max(self.depth, *(y for _, y in path))
        prev = path[0]
        self.add(tuple(prev))
        for xy in path[1:]:
            index = prev[0] == xy[0]
            diff = xy[index] - prev[index]
            sign = diff // abs(diff)
            for i in range(prev[index], xy[index], sign):
                prev[index] = i + sign
                self.add(tuple(prev))
    
    def next_sand(self):
        if self.source in self:
            return
        prev = self.source
        while prev[1] < self.depth + 1:
            steps = Cave.sand_step(prev)
            for xy in steps:
                if xy not in self:
                    prev = xy
                    break
            if prev != xy:
                self.add(prev)
                return prev
        self.add(prev)
        return prev

    def sand_step(xy):
        x, y = xy
        y += 1
        return ((x, y), (x - 1, y), (x + 1, y))

cave = Cave()
with open("input") as f:
    for line in f.readlines():
        path = line.rstrip().split(" -> ")
        path = [[int(s) for s in xy.split(',')] for xy in path]
        cave.add_path(path)
    
count = 0
while cave.next_sand():
    count += 1
print(count)
