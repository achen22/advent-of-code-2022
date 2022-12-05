stacks = {1: ''}
with open("input") as f:
    line = f.readline()[:-1]
    while line:
        i = 0
        while line:
            assert len(line) == 3 or line[3] == ' '
            i += 1
            crate = line[:3]
            line = line[4:]
            if crate[0] != ' ':
                if i in stacks:
                    stacks[i] += crate[1]
                else:
                    stacks[i] = crate[1]
        line = f.readline()[:-1]
    
    #print(stacks)
    for line in f.readlines():
        line = line.split(' ')
        c = int(line[1])
        si = int(line[3])
        di = int(line[5])
        stack = stacks[si][:c]
        stacks[si] = stacks[si][c:]
        #stack = stack[::-1]
        stacks[di] = stack + stacks[di]
        #print(stacks)

first = (stacks[i + 1][0] for i in range(len(stacks)))
print(''.join(first))