import json

code = open('code.asm', 'r').read()

codeLines = code.split('\n')

machinecode = []
newlines = []
toOffset = []
changejump = []

for i in range(len(codeLines)):
    codeLines[i] = codeLines[i].strip()
    newlines.append(len(machinecode))
    if codeLines[i] == '' or codeLines[i][0:2] == '//':
        continue
    if codeLines[i][0:3] == 'ADD':
        # add command
        params = codeLines[i][4:].split(',')
        machinecode.append(1)
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
        machinecode.append(int(params[2]))
    if codeLines[i][0:3] == 'SUB':
        # add command
        params = codeLines[i][4:].split(',')
        machinecode.append(2)
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
        machinecode.append(int(params[2]))
    elif codeLines[i][0:3] == 'MUL':
        # multiply command
        params = codeLines[i][4:].split(',')
        machinecode.append(3)
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
        machinecode.append(int(params[2]))
    elif codeLines[i][0:3] == 'INP':
        # input command
        params = codeLines[i][4:].split(',')
        machinecode.append(4)
        machinecode.append(int(params[0]))
    elif codeLines[i][0:3] == 'OUT':
        # output command
        params = codeLines[i][4:].split(',')
        machinecode.append(5)
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'JIT':
        # jump if true command
        params = codeLines[i][4:].split(',')
        machinecode.append(6)
        machinecode.append(int(params[0]))
        changejump.append(len(machinecode))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'JIF':
        # jump if false command
        params = codeLines[i][4:].split(',')
        machinecode.append(7)
        machinecode.append(int(params[0]))
        changejump.append(len(machinecode))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'REL':
        # register load command
        params = codeLines[i][4:].split(',')
        machinecode.append(8)
        machinecode.append(int(params[0]))
        toOffset.append(len(machinecode))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'MEL':
        # memory load command
        params = codeLines[i][4:].split(',')
        machinecode.append(9)
        toOffset.append(len(machinecode))
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'RES':
        # register set command
        params = codeLines[i][4:].split(',')
        machinecode.append(10)
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'MES':
        # memory set command
        params = codeLines[i][4:].split(',')
        machinecode.append(11)
        toOffset.append(len(machinecode))
        machinecode.append(int(params[0]))
        machinecode.append(int(params[1]))
    elif codeLines[i][0:3] == 'SLE':
        # snooze command
        params = codeLines[i][4:].split(',')
        machinecode.append(12)
        machinecode.append(int(params[0]))
    else:
        # invalid command
        raise Exception("Invalid command")

offset = len(machinecode)+1

for i in range(len(toOffset)):
    machinecode[toOffset[i]] += offset

for i in range(len(changejump)):
  machinecode[changejump[i]] = (newlines[machinecode[changejump[i]]-1])
print(machinecode)

file = open('machinecode.exe', 'w')
for i in range(len(machinecode)):
  file.write(chr(machinecode[i]))
