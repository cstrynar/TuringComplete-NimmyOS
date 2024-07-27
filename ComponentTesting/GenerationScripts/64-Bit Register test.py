import random
import time

# This is for use with the "64-Bit Register Test" schematic in the Lab.
# The following assembly codes are assumed:
#   LoadInput == 2
#   LoadAndSave == 3

startTime = time.time()

outputDir = 'ComponentTesting/Output'
outputFile = '64-Bit Register test.txt'

numTests = 100
# values passed into the input are in 2's complement notation
minVal = -2**63
maxVal = 2**63 - 1

# in order to test, we must simulate a register ourselves
# this var contains the value that should be in the register at all times
val = 0

lines = []

for i in range(numTests):
    randNum = random.randint(minVal, maxVal)
    testType = random.randint(0, 1)
    # a testType of 0 means we will load the input, but not save it.
    # a testType of 1 means we will load and save the input.
    
    if testType == 0:
        lines.append(f'# test {i+1}: Load Without Save\n')
        lines.append(f'set_input {randNum}\n')
        lines.append('LoadInput\n')
        lines.append(f'expect 0 {val}\n\n')
    elif testType == 1:
        val = randNum
        lines.append(f'# test {i+1}: Load And Save\n')
        lines.append(f'set_input {randNum}\n')
        lines.append('LoadAndSave\n')
        lines.append(f'expect 0 {val}\n\n')
    

# the testing lab in TC expects the program memory to be incremented by 4 bytes instead of 1, and the test stops when it sees the next four bytes are all zero.
# if we don't append four bytes of "do nothing", it will not run our last four instructions.
lines.append('1 1 1 1')

with open(f'{outputDir}/{outputFile}', 'w+') as f:
    f.writelines(lines)

print(f'Lab program file generated. Outputted to {outputDir}/{outputFile}')
print(f'Generation runtime: {time.time() - startTime}')
