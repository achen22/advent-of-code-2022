from itertools import combinations

LIMIT = 24
Plan = tuple[int, int, int]

class Path:
    def __init__(self, blueprint: tuple[Plan, Plan, Plan, Plan]):
        self.blueprint = blueprint
        self.path: list[int] = []
        self.robots = [1, 0, 0, 0]
        self.materials = [0, 0, 0, 0]
        self.turns = 0

    def clone(self):
        other = Path(self.blueprint)
        other.path = self.path[:]
        other.robots = self.robots[:]
        other.materials = self.materials[:]
        other.turns = self.turns
        return other
    
    def do_turn(self, turns = 1):
        self.turns += turns
        for i in range(4):
            self.materials[i] += self.robots[i] * turns
    
    def build(self, n: int):
        assert n >= 0 and n <= 3
        if n >= 2:
            if self.robots[n - 1] == 0:
                return False
        
        plan = self.blueprint[n]
        turns = -min((m - p) // r for m, p, r in zip(self.materials, plan, self.robots) if r != 0)
        if turns < 0:
            turns = 0
        self.do_turn(turns + 1)
        
        self.path.append(n)
        self.robots[n] += 1
        for i in range(len(plan)):
            self.materials[i] -= plan[i]
        return True

blueprints = []
with open("input") as f:
    for line in f.readlines():
        id, blueprint = line.rstrip().split(": ")
        id = int(id.split(' ')[1])
        ore, clay, obsidian, geode = (s.split() for s in blueprint.split(". "))

        assert ore[1] == "ore" and ore[5] == "ore"
        ore = (int(ore[4]), 0, 0)

        assert clay[1] == "clay" and clay[5] == "ore"
        clay = (int(clay[4]), 0, 0)

        assert obsidian[1] == "obsidian" and obsidian[5] == "ore" and obsidian[8] == "clay"
        obsidian = (int(obsidian[4]), int(obsidian[7]), 0)

        assert geode[1] == "geode" and geode[5] == "ore" and geode[8] == "obsidian."
        geode = (int(geode[4]), 0, int(geode[7]))

        blueprints.append((ore, clay, obsidian, geode))
        assert len(blueprints) == id

total = 0
for i in range(len(blueprints)):
    robot_max = tuple(max(resource) for resource in zip(*blueprints[i]))
    paths = [Path(blueprints[i])]
    highest = 0
    while paths:
        group: dict[tuple[int, int, int, int], list[Path]] = {}
        for path in paths:
            k = tuple(path.robots)
            if k in group:
                group[k].append(path)
            else:
                group[k] = [path]
        prev = paths
        for paths in group.values():
            remove = []
            for a, b in combinations(paths, 2):
                if a in remove or b in remove:
                    continue
                turns = b.turns - a.turns
                if turns < 0:
                    a, b = b, a
                    turns = -turns
                materials = tuple(m + turns * r for m, r in zip(a.materials, a.robots))
                if all(m1 >= m2 for m1, m2 in zip(materials, b.materials)):
                    remove.append(b)
                elif turns == 0 and all(m1 <= m2 for m1, m2 in zip(materials, b.materials)):
                    remove.append(a)
            for path in remove:
                prev.remove(path)

        paths = []
        for path in prev:
            for n in range(4):
                if n != 3 and path.robots[n] == robot_max[n]:
                    continue
                step = path.clone()
                result = step.build(n)
                if result and step.turns < LIMIT:
                    geode = step.materials[3]
                    robots = step.robots[3]
                    turns = LIMIT - step.turns
                    if n == 3:
                        end = geode + robots * turns
                        if end > highest:
                            highest = end
                            #print(end)
                    potential = turns + robots
                    potential *= (potential - 1)
                    potential //= 2
                    if potential + geode <= highest:
                        continue
                    paths.append(step)
    print(i + 1, highest)
    total += highest * (i + 1)

print(total)
