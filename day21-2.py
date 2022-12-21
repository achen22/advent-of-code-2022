OPERATION = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b
}

SOLVE = {
    "+": (lambda b, c: c - b, lambda a, c: c - a),
    "-": (lambda b, c: b + c, lambda a, c: a - c),
    "*": (lambda b, c: c // b, lambda a, c: c // a),
    "/": (lambda b, c: b * c, lambda a, c: a // c)
}

def find(name, monkeys, numbers):
    if name == "humn":
        return "humn"
    if name in numbers:
        return numbers[name]
    a, op, b = monkeys[name]
    a = find(a, monkeys, numbers)
    b = find(b, monkeys, numbers)
    if type(a) == int and type(b) == int:
        result = OPERATION[op](a, b)
        numbers[name] = result
        return result
    return (a, op, b)

def solve(expression, number):
    a, op, b = expression
    if type(a) == int:
        op = SOLVE[op][1]
        number = op(a, number)
        expression = b
    else:
        assert type(b) == int
        op = SOLVE[op][0]
        number = op(b, number)
        expression = a
    return (expression, number)

monkeys = {}
numbers = {}
with open("input") as f:
    for line in f.readlines():
        name, number = line.rstrip().split(": ")
        assert name not in numbers and name not in monkeys
        if name == "root":
            hvalue, _, mvalue = number.split(' ')
        elif name == "humn":
            continue
        elif number.isdigit():
            numbers[name] = int(number)
        else:
            monkeys[name] = number.split(' ')

mvalue = find(mvalue, monkeys, numbers)
hvalue = find(hvalue, monkeys, numbers)
if type(hvalue) == int:
    hvalue, mvalue = mvalue, hvalue
while hvalue != "humn":
    hvalue, mvalue = solve(hvalue, mvalue)

print(mvalue)
