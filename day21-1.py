OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b
}

monkeys = {}
numbers = {}
with open("input") as f:
    for line in f.readlines():
        name, number = line.rstrip().split(": ")
        assert name not in numbers and name not in monkeys
        if number.isdigit():
            numbers[name] = int(number)
        else:
            monkeys[name] = number.split(' ')

findlist = ["root"]
while findlist:
    name = findlist.pop()
    a, op, b = monkeys[name]
    missing = [c for c in (a, b) if c not in numbers]
    if missing:
        findlist.append(name)
        findlist.extend(missing)
    else:
        a = numbers[a]
        b = numbers[b]
        numbers[name] = OPERATIONS[op](a, b)

print(numbers["root"])
