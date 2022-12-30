SNAFU = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2',
}

UNSNAFU = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

def snafu(n: int):
    if n == 0:
        return SNAFU[0]
    result = ""
    while n != 0:
        r = n % 5
        if r > 2:
            r -= 5
            n += 5
        result = SNAFU[r] + result
        n //= 5
    return result

def unsnafu(s: str):
    result = 0
    for c in s:
        result *= 5
        result += UNSNAFU[c]
    return result

total = 0
with open("input") as f:
    for line in f.readlines():
        total += unsnafu(line.rstrip())

print(snafu(total))