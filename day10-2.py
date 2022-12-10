WIDTH = 40
HEIGHT = 6
pixels = [""]

def write_pixel(cycle, x):
    pixels[-1] += '#' if abs(x - (cycle - 1) % WIDTH) <= 1 else '.'
    if len(pixels[-1]) == WIDTH:
        if len(pixels) == HEIGHT:
            return True
        pixels.append("")
    return False

with open("input") as f:
    cycle = 1
    x = 1
    for line in f.readlines():
        line = line.rstrip()
        if write_pixel(cycle, x):
            break
        cycle += 1
        if line == "noop":
            continue
        # line[:4] == "addx"
        if write_pixel(cycle, x):
            break
        cycle += 1
        x += int(line[5:])

print('\n'.join(pixels))
