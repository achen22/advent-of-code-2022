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

    def find_reverse_path_by_z(self, end = None, z = 0):
        if end == None:
            end = self.end
        scoring = tuple(node for node in self.get_neighbours(end) if end.z <= node.z + 1)
        visited = {node.xy: 1 for node in scoring}
        visited[end.xy] = 0
        scored = {node.xy: abs(node.z - z) + 1 for node in scoring}
        while len(scored) != 0:
            min_score = min(scored.values())
            for xy in scored:
                if scored[xy] == min_score:
                    current = self.nodes[xy]
                    del(scored[xy])
                    break
            scoring = (node for node in self.get_neighbours(current) if current.z <= node.z + 1)
            path = visited[xy] + 1
            for node in scoring:
                if node.z == z:
                    return path
                xy = node.xy
                if xy in visited and visited[xy] <= path:
                    continue
                visited[xy] = path
                scored[xy] = path + abs(node.z - z)
        return -1
    
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

print(hmap.find_reverse_path_by_z())