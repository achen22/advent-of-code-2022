class Dir:
    def __init__(self, parent = None):
        self.parent = parent
        self.contents = {}

    def put(self, name, content):
        content = Dir(self) if content == "dir" else int(content)
        self.contents[name] = content
    
    def get(self, name):
        return self.parent if name == ".." else self.contents[name]
    
    def size(self):
        return sum(c.size() if type(c) == Dir else c for c in self.contents.values())

    def __str__(self, indent = 0):
        prefix = " " * indent
        result = []
        for name, content in self.contents.items():
            if type(content) == Dir:
                result.append(f"{prefix}- {name} (dir)")
                result.append(content.__str__(indent + 2))
            else:
                result.append(f"{prefix}- {name} (file, size={content})")
        return '\n'.join(result)

Dir.root = Dir()
dirs = set()
dirs.add(Dir.root)

with open("input") as f:
    cd = Dir.root
    assert f.readline()[:-1] == "$ cd /"
    line = f.readline()[:-1].split(' ')
    while line[0]:
        if line[1] == "cd":
            cd = cd.get(line[2])
            dirs.add(cd)
            line = f.readline()[:-1].split(' ')
        else:
            assert len(line) == 2 and line[1] == "ls"
            line = f.readline()[:-1].split(' ')
            while line[0] and line[0] != "$":
                cd.put(line[1], line[0])
                line = f.readline()[:-1].split(' ')

#print(Dir.root)
print(sum(d.size() for d in dirs if d.size() <= 100000))
