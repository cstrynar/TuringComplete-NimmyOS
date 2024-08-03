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

# values passed into the input are in 2's complement notation
minVal = -2**63
maxVal = 2**63 - 1

# the min and max vals used for low-range testing (inclusive)
lowRangeMinVal = -100
lowRangeMaxVal = 100

edgeCaseValues = [0, 1, -1, minVal, maxVal]  # these are the values used in checking edge cases.
                                             # we test every combination of the values in this list for the edge case tests
numRandomTests = 25                          # this is the number of random tests to run for each value-range for each operation.

global lines
lines = []


def Generate1InputOpcodeTest(input1: int, output: int):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output}\n\n')


def Generate2InputOpcodeTest(input1: int, input2: int, output: int):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append(f'set_input {input2}\n')
    lines.append('SaveInput2\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output}\n\n')


def Generate1InputIntegerOpcodeTest(input1: int, output: tuple[int, int, int]):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output[0]}\n')
    lines.append(f'expect 2 {output[1]}\n')
    lines.append(f'expect 3 {output[2]}\n\n')


def Generate2InputIntegerOpcodeTest(input1: int, input2: int, output: tuple[int, int, int]):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append(f'set_input {input2}\n')
    lines.append('SaveInput2\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output[0]}\n')
    lines.append(f'expect 2 {output[1]}\n')
    lines.append(f'expect 3 {output[2]}\n\n')


def GenerateBitwiseOpsTest():
    global lines
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

    singleInputOperationList = ['NOT']

    lines.append('# Bitwise Operations\n')

    startOpcode = 1
    for i in range(len(functionList)):
        lines.append(f'# Opcode {i + startOpcode}: {functionList[i][0]}\n')
        lines.append(f'set_input {i+startOpcode}\n')
        lines.append('SaveOpcode\n\n')

        testCount = 1  # keep track of how many tests we do

        if (functionList[i][0] in singleInputOperationList):
            # single input ops
            # do edge cases
            for j in edgeCaseValues:
                lines.append(f'# test {testCount}: edge case\n')
                Generate1InputOpcodeTest(j, functionList[i][1](j))
                testCount += 1

            # do low-range random cases
            for j in range(numRandomTests):
                num1 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                lines.append(f'# test {testCount}: random low-range\n')
                Generate1InputOpcodeTest(num1, functionList[i][1](num1))
                testCount += 1

            # do random cases
            for j in range(numRandomTests):
                num1 = random.randint(minVal, maxVal) 
                lines.append(f'# test {testCount}: random\n')
                Generate1InputOpcodeTest(num1, functionList[i][1](num1))
                testCount += 1
        else:
            # two input ops
            # do edge cases
            for j in edgeCaseValues:
                for k in edgeCaseValues:
                    lines.append(f'# test {testCount}: edge case\n')
                    Generate2InputOpcodeTest(j, k, functionList[i][1](j, k))
                    testCount += 1
            
            # do low-range random cases
            for j in range(numRandomTests):
                num1 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                num2 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                lines.append(f'# test {testCount}: random low-range\n')
                Generate2InputOpcodeTest(num1, num2, functionList[i][1](num1, num2))
                testCount += 1

            # do random cases
            for j in range(numRandomTests):
                num1 = random.randint(minVal, maxVal)
                num2 = random.randint(minVal, maxVal)
                lines.append(f'# test {testCount}: random\n')
                Generate2InputOpcodeTest(num1, num2, functionList[i][1](num1, num2))
                testCount += 1

    lines.append('1 1 1 1')

    with open(f'{outputDir}/{outputFile}', 'w+') as f:
        f.writelines(lines)

    print(f'Lab program file generated. Outputted to {outputDir}/{outputFile}')
    print(f'Generation runtime: {time.time() - startTime}')

    # clear lines
    lines = []


def GenerateIntegerOpsTest():
    global lines
    startTime = time.time()

    outputFile = 'Integer Operations test.txt'

    # these tests *also* have to worry about the overflow and divideByZero flags. each function returns a tuple with the answer, and the overflow flag, and the divideByZero flag.
    functionList = [('Negate', MathUtility.IntegerNegate),
                    ('Unsigned Addition', MathUtility.UnsignedAddition),
                    ('Signed Addition', MathUtility.SignedAddition),
                    ('Unsigned Subtraction', MathUtility.UnsignedSubtraction),
                    ('Signed Subtraction', MathUtility.SignedSubtraction),
                    ('Unsigned Multiplication', MathUtility.UnsignedMultiplication),
                    ('Signed Multiplication', MathUtility.SignedMultiplication),
                    ('Unsigned Integer Division', MathUtility.UnsignedIntegerDivision),
                    ('Unsigned Integer Modulo', MathUtility.UnsignedIntegerModulo),
                    ('Signed Integer Division', MathUtility.SignedIntegerDivision),
                    ('Signed Integer Modulo', MathUtility.SignedIntegerModulo),
                    ('Unsigned Integer to Float', MathUtility.UnsignedIntegerToFloat),
                    ('Signed Integer to Float',  MathUtility.SignedIntegerToFloat),
                    ('Unsigned Integer to Double', MathUtility.UnsignedIntegerToDouble),
                    ('Signed Integer to Double', MathUtility.SignedIntegerToDouble)
                    ]
    
    singleInputOperationList = ['Negate', 'Unsigned Integer to Float', 'Signed Integer to Float', 'Unsigned Integer to Double', 'Signed Integer to Double']

    lines.append('# Integer Operations\n')

    # integer ops take up opcodes from 16-30 inclusive
    startOpcode = 16
    for i in range(len(functionList)):
        lines.append(f'# Opcode {i+startOpcode}: {functionList[i][0]}\n')
        lines.append(f'set_input {i+startOpcode}\n')
        lines.append('SaveOpcode\n\n')

        testCount = 1  # keep track of how many tests we do

        if (functionList[i][0] in singleInputOperationList):
            # single input ops
            # do edge cases
            for j in edgeCaseValues:
                lines.append(f'# test {testCount}: edge case\n')
                Generate1InputIntegerOpcodeTest(j, functionList[i][1](j))
                testCount += 1

            # do low-range random cases
            for j in range(numRandomTests):
                num1 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                lines.append(f'# test {testCount}: random low-range\n')
                Generate1InputIntegerOpcodeTest(num1, functionList[i][1](num1))
                testCount += 1

            # do random cases
            for j in range(numRandomTests):
                num1 = random.randint(minVal, maxVal) 
                lines.append(f'# test {testCount}: random\n')
                Generate1InputIntegerOpcodeTest(num1, functionList[i][1](num1))
                testCount += 1
        else:
            # two input ops
            # do edge cases
            for j in edgeCaseValues:
                for k in edgeCaseValues:
                    lines.append(f'# test {testCount}: edge case\n')
                    Generate2InputIntegerOpcodeTest(j, k, functionList[i][1](j, k))
                    testCount += 1
            
            # do low-range random cases
            for j in range(numRandomTests):
                num1 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                num2 = random.randint(lowRangeMinVal, lowRangeMaxVal)
                lines.append(f'# test {testCount}: random low-range\n')
                Generate2InputIntegerOpcodeTest(num1, num2, functionList[i][1](num1, num2))
                testCount += 1

            # do random cases
            for j in range(numRandomTests):
                num1 = random.randint(minVal, maxVal)
                num2 = random.randint(minVal, maxVal)
                lines.append(f'# test {testCount}: random\n')
                Generate2InputIntegerOpcodeTest(num1, num2, functionList[i][1](num1, num2))
                testCount += 1
    
    lines.append('1 1 1 1')

    with open(f'{outputDir}/{outputFile}', 'w+') as f:
        f.writelines(lines)

    print(f'Lab program file generated. Outputted to {outputDir}/{outputFile}')
    print(f'Generation runtime: {time.time() - startTime}')

    # clear lines
    lines = []
            

GenerateBitwiseOpsTest()
GenerateIntegerOpsTest()


print(f'Total runtime: {time.time() - globalStartTime}')





