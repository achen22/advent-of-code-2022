from itertools import combinations

class Game:
    TURNS = 26
    START = "AA"

    def __init__(self, nodes = None):
        self.valve = Valve.valves[Game.START]
        self.path = []
        self.score = 0
        self.turns = Game.TURNS
        if nodes != None:
            for node in nodes:
                if not self.goto(node):
                    break
    
    def goto(self, name):
        self.turns -= self.valve.dist_to[name]
        if self.turns <= 0:
            return False
        self.valve = Valve.valves[name]
        if name not in self.path:
            self.turns -= 1
            self.score += self.turns * self.valve.rate
        self.path.append(name)
        return self.turns != 0
    
    def clone(self):
        result = Game()
        result.valve = self.valve
        result.path.extend(self.path)
        result.score = self.score
        result.turns = self.turns
        return result

class Valve:
    valves = {}

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.is_open = False
        self.tunnels = []
        self.dist_to = {}
        Valve.valves[name] = self
    
    def calc_dist():
        for name, valve in Valve.valves.items():
            valve.dist_to[name] = 0
            tunnels = set(valve.tunnels)
            dist = 1
            while tunnels:
                prev = tuple(tunnels)
                tunnels.clear()
                for other in prev:
                    valve.dist_to[other] = dist
                    tunnels.update(v for v in Valve.valves[other].tunnels if v not in valve.dist_to)
                dist += 1

with open("input") as f:
    for line in f.readlines():
        line = line.rstrip().split(' ', 9)
        rate = line[4]
        assert rate[:5] == "rate="
        rate = int(rate[5:-1])
        Valve(line[1], rate).tunnels.extend(line[9].split(", "))
Valve.calc_dist()

working = (v for v in Valve.valves.values() if v.rate != 0)
working = sorted(working, key = lambda v: v.rate, reverse = True)
working = tuple(v.name for v in working)

games = {(): Game()}
scores = {}
while games:
    game = max((g for g in games.values()), key = lambda g: g.turns)
    for name in working:
        if name in game.path:
            continue
        step = game.clone()
        success = step.goto(name)
        ordered = tuple(sorted(step.path) + [name])
        if ordered in scores:
            prev = scores[ordered]
            if prev.score >= step.score:
                continue
            prev = tuple(prev.path)
            if prev in games:
                del games[prev]
        scores[ordered] = step
        if success:
            games[tuple(step.path)] = step
    del games[tuple(game.path)]

reduced = {}
for t, g in scores.items():
    t = t[:-1]
    if t in reduced:
        if reduced[t].score >= g.score:
            continue
    reduced[t] = g

highest = 0
for a, b in combinations(reduced.keys(), 2):
    if set(a).intersection(b):
        continue
    a, b = (reduced[i] for i in (a, b))
    score = a.score + b.score
    if score > highest:
        highest = a.score + b.score
        print(highest, a.path, b.path)
