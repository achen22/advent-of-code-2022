class Heightmap:
    def __init__(self):
        self.start = Node(0, 0, 0)
        self.end = self.start
        self.nodes = {(self.end.xy): self.end}
        self.width = 1
        self.length = 1
    
    def add(self, node):
        self.nodes[node.xy] = node
        self.width = max(node.x + 1, self.width)
        self.length = max(node.y + 1, self.length)
    
    def get_neighbours(self, node):
        x, y = node.xy
        neighbours = ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))
        return tuple(self.nodes[xy] for xy in neighbours if xy in self.nodes)

    def find_path(self, start = None, end = None):
        if start == None:
            start = self.start
        if end == None:
            end = self.end
        scoring = tuple(node for node in self.get_neighbours(start) if node.z <= start.z + 1)
        visited = {node.xy: 1 for node in scoring}
        visited[start.xy] = 0
        scored = {node.xy: self.min_path_length(node) + 1 for node in scoring}
        while end.xy not in visited:
            min_score = min(scored.values())
            for xy in scored:
                if scored[xy] == min_score:
                    current = self.nodes[xy]
                    del(scored[xy])
                    break
            scoring = (node for node in self.get_neighbours(current) if node.z <= current.z + 1)
            path = visited[xy] + 1
            for node in scoring:
                xy = node.xy
                if xy in visited and visited[xy] <= path:
                    continue
                visited[xy] = path
                scored[xy] = path + self.min_path_length(node)
        return visited[end.xy]
    
    def min_path_length(self, start = None, end = None):
        if start == None:
            start = self.start
        if end == None:
            end = self.end
        return max(end.z - start.z, abs(end.x - start.x) + abs(end.y - start.y))

class Node:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def xy(self):
        return (self.x, self.y)

hmap = Heightmap()
with open("input") as f:
    j = 0
    line = f.readline().rstrip()
    while line:
        for i in range(len(line)):
            c = line[i]
            if c == 'S':
                node = Node(i, j, 0)
                hmap.add(node)
                hmap.start = node
            elif c == 'E':
                node = Node(i, j, 25)
                hmap.add(node)
                hmap.end = node
            else:
                hmap.add(Node(i, j, ord(c) - ord('a')))
        j += 1
        line = f.readline().rstrip()

print(hmap.find_path())