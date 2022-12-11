def increase_by(n):
    return lambda x: x + n

def multiply_by(n):
    return lambda x: x * n

def square():
    return lambda x: x * x

class Item:
    tests = set()

    def __init__(self, item):
        self.test = {n: item % n for n in Item.tests}
    
    def apply(self, operation):
        self.test = {n: operation(self.test[n]) % n for n in Item.tests}

class Monkey:
    monkeys = []

    def __init__(self, notes):
        assert notes["Monkey"] == len(Monkey.monkeys)
        self.id = notes["Monkey"]
        Monkey.monkeys.append(self)

        self.items = [int(s) for s in notes["Starting items"].split(", ")]
        self.count = 0

        operation = notes["Operation"]
        assert operation[:10] == "new = old "
        operation = operation[10:].split(' ')
        if operation[0] == '+':
            self.operation = increase_by(int(operation[1]))
        else:
            assert operation[0] == '*'
            self.operation = square() if operation[1] == "old" else multiply_by(int(operation[1]))
        
        assert notes["Test"][:13] == "divisible by "
        self.test = int(notes["Test"][13:])
        Item.tests.add(self.test)

        assert notes["If true"][:16] == "throw to monkey "
        assert notes["If false"][:16] == "throw to monkey "
        self.target = (int(notes["If false"][16:]), int(notes["If true"][16:]))
    
    def throw_items(self):
        while self.items:
            self.count += 1
            item = self.items.pop(0)
            if type(item) == int:
                item = Item(item)
            item.apply(self.operation)
            other = Monkey.monkeys[self.target[item.test[self.test] == 0]]
            other.items.append(item)
    
    def do_rounds(n, verbose = False):
        for i in range(n):
            for m in Monkey.monkeys:
                m.throw_items()
            if not verbose:
                continue
            print(f"After round {i+1}:")
            for m in Monkey.monkeys:
                print(f"Monkey {m.id}: " + ", ".join(str(it) for it in m.items))
            print()

with open("input") as f:
    notes = {}
    for line in f.readlines():
        if line.isspace():
            Monkey(notes)
            notes = {}
        elif line[0] == 'M':
            notes["Monkey"] = int(line.rstrip()[7:-1])
        else:
            line = line.strip().split(": ")
            notes[line[0]] = line[1]
    if notes:
        Monkey(notes)

Monkey.do_rounds(10000)
counts = sorted((m.count for m in Monkey.monkeys), reverse=True)
print(counts[0] * counts[1])