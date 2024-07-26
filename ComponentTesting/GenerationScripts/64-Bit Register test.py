import random
import time

startTime = time.time()

outputDir = 'ComponentTesting/Output'
outputFile = '64-Bit Register test.txt'

numTests = 100
# values passed into the input are in 2's complement notation
minVal = -2**63
maxVal = 2**63 - 1


lines = []

for i in range(numTests):
    randNum = random.randint(minVal, maxVal)
    lines.append(f'set_input {randNum}\n')
    lines.append('1\n')
    lines.append(f'expect 0 {randNum}\n')

lines.append('2\n')
lines.append('expect 0 0\n')
lines.append('2\n')
lines.append('2\n')
lines.append('2\n')

with open(f'{outputDir}/{outputFile}', 'w+') as f:
    f.writelines(lines)

print(f'Lab program file generated. Outputted to {outputDir}/{outputFile}')
print(f'Generation runtime: {time.time() - startTime}')

