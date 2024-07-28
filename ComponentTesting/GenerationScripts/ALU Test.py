import random
import time
from ..Utility import MathUtility

# This is for use with the "ALU Test" schematic in the Lab.
# The following assembly codes are assumed:
#   SaveOpcode == 2
#   SaveInput1 == 3
#   SaveInput2 == 4
#   SaveOutput == 5

globalStartTime = time.time()

outputDir = 'ComponentTesting/Output'

numTests = 50  # this is the number of tests to run per operation
# values passed into the input are in 2's complement notation
minVal = -2**63
maxVal = 2**63 - 1

lines = ['# Bitwise Operations\n']


def Generate1InputOpcodeTest(input1: int, output: int):
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output}\n\n')


def Generate2InputOpcodeTest(input1: int, input2: int, output: int):
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append(f'set_input {input2}\n')
    lines.append('SaveInput2\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output}\n\n')


def GenerateBitwiseOpsTest():
    startTime = time.time()

    outputFile = 'Bitwise Operations test.txt'

    functionList = [('AND',  lambda x,y:  x&y),
                    ('OR',   lambda x,y:  x|y),
                    ('NOR',  lambda x,y:  ~(x|y)),
                    ('XOR',  lambda x,y:  x^y),
                    ('NAND', lambda x,y:  ~(x&y)),
                    ('XNOR', lambda x,y:  ~(x^y)),
                    ('NOT',  lambda x:    ~x),
                    ('SHL',  lambda x,y:  MathUtility.SHL(x, y)),
                    ('SHR',  lambda x,y:  MathUtility.SHR(x, y)),
                    ('ROTL', lambda x,y:  MathUtility.ROTL(x, y)),
                    ('ROTR', lambda x,y:  MathUtility.ROTR(x, y)),
                    ('ASHR', lambda x,y:  MathUtility.ASHR(x, y))]

    # go through all 11 bitwise operations, and generate random tests
    for i in range(len(functionList)):
        lines.append(f'# Opcode {i+1}: {functionList[i][0]}\n')
        lines.append(f'set_input {i+1}\n')
        lines.append('SaveOpcode\n')

        for j in range(numTests):
            num1 = random.randint(minVal, maxVal)
            if functionList[i][0] in ['SHL', 'SHR', 'ASHR']:
                num2 = random.randint(-100, 100)   # restricting the range on the second num is much better for testing SHL and SHR
                                                # Also, negatives are not allowed in python shift operations, but 
            else:
                num2 = random.randint(minVal, maxVal)
            
            lines.append(f'# test {j+1}\n')
            if functionList[i][0] == 'NOT':
                Generate1InputOpcodeTest(num1, functionList[i][1](num1))
            else:
                Generate2InputOpcodeTest(num1, num2, functionList[i][1](num1, num2))

    lines.append('1 1 1 1')

    with open(f'{outputDir}/{outputFile}', 'w+') as f:
        f.writelines(lines)

    print(f'Lab program file generated. Outputted to {outputDir}/{outputFile}')
    print(f'Generation runtime: {time.time() - startTime}')


GenerateBitwiseOpsTest()

print(f'Total runtime: {time.time() - globalStartTime}')





