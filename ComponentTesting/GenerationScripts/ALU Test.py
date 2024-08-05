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

defaultOutputDir = 'ComponentTesting/Output'

# values passed into the input are in 2's complement notation
minVal = -2**63
maxVal = 2**63 - 1

# the min and max vals used for low-range testing (inclusive)
lowRangeMinVal = -100
lowRangeMaxVal = 100

defaultEdgeCaseValues = [0, 1, -1, minVal, maxVal]  # these are the values used in checking edge cases.
                                             # we test every combination of the values in this list for the edge case tests
defaultNumRandomTests = 25                          # this is the number of random tests to run for each value-range for each operation.

defaultTestRanges = {'Random Low-Range': (lowRangeMinVal, lowRangeMaxVal), 'Random': (minVal, maxVal)}

global lines
lines = []

def Generate1InputALUTest(input1: int, output: tuple[int, int]):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output[0]}\n')
    lines.append(f'expect 1 {output[1]}\n\n')


def Generate2InputALUTest(input1: int, input2: int, output: tuple[int, int]):
    global lines
    lines.append(f'set_input {input1}\n')
    lines.append('SaveInput1\n')
    lines.append(f'set_input {input2}\n')
    lines.append('SaveInput2\n')
    lines.append('SaveOutput\n')
    lines.append(f'expect 0 {output[0]}\n')
    lines.append(f'expect 1 {output[1]}\n\n')
            

# generate LAB testing file for a set of ALU operations
def GenerateALUTest(testTitle:str,                                              # string to display as comment at top of output (eg 'Integer Operations')
                    outputFile:str,                                             # name of output file
                    operationDict:dict[str, tuple[int,callable]],               # mapping of operation names -> opcode, test function 
                                                                                #   function should return both expected output and expected flag bits
                    singleInputOps:list[str],                                   # list of operations in functionDict that only take a single input
                    outputDir:str=defaultOutputDir,                             
                    edgeValues:list[int]=defaultEdgeCaseValues,                 # every combination of edgee cases is tested
                    numRandomTests:int=defaultNumRandomTests,                   # how many random tests to do for each range
                    testRanges:dict[str, tuple[int, int]]=defaultTestRanges):   # mapping of range names -> (minVal, maxVal)
    
    # ensure functionDict is nonempty
    if (len(operationDict) == 0):
        raise ValueError('operationDict cannot be empty.')

    # ensure singleInputOps are all present in functionDict
    for op in singleInputOps:
        if op not in operationDict:
            raise LookupError(f'single input operation {op} not found in functionDict.')
    
    # track start time
    startTime = time.time()

    # clear global lines variable
    # this is global so helper-functions can write lines without needing to pass around a list as input/output
    global lines
    lines = []

    lines.append(f'# {testTitle}\n\n')

    # start with one input operations, then do two input operations
    # start with edge cases, then do all of the random tests using the ranges specified in testRanges
    if len(singleInputOps) != 0:
        lines.append('# Single Input Operation Tests:\n')
    
    for op in singleInputOps:
        opcode = operationDict[op][0]
        testFunc = operationDict[op][1]

        lines.append(f'# Opcode {opcode}: {op}\n')
        lines.append(f'set_input {opcode}\n')
        lines.append('SaveOpcode\n\n')

        testCount = 1

        # edge cases
        for val in edgeValues:
            lines.append(f'# test {testCount}: Edge Case\n')
            Generate1InputALUTest(val, testFunc(val))
            testCount += 1
        
        # random cases
        for r in testRanges:
            lowVal = testRanges[r][0]
            highVal = testRanges[r][1]
            lines.append(f'# {r}: ({lowVal}, {highVal})\n')

            for i in range(numRandomTests):
                lines.append(f'# test {testCount}: {r}\n')
                val1 = random.randint(lowVal, highVal)
                Generate1InputALUTest(val1, testFunc(val1))
                testCount += 1
        
    
    # two input operations
    twoInputOperations = list(op for op in operationDict if op not in singleInputOps)
    if (twoInputOperations != 0):
        lines.append('# Double Input Operation Tests:\n')
    
    for op in twoInputOperations:
        opcode = operationDict[op][0]
        testFunc = operationDict[op][1]

        lines.append(f'# Opcode {opcode}: {op}\n')
        lines.append(f'set_input {opcode}\n')
        lines.append('SaveOpcode\n\n')

        testCount = 1

        # edge cases
        for val1 in edgeValues:
            for val2 in edgeValues:
                lines.append(f'# test {testCount}: Edge Case\n')
                Generate2InputALUTest(val1, val2, testFunc(val1, val2))
                testCount += 1
        
        # random cases
        for r in testRanges:
            lowVal = testRanges[r][0]
            highVal = testRanges[r][1]
            lines.append(f'# {r}: ({lowVal}, {highVal})\n')

            for i in range(numRandomTests):
                lines.append(f'# test {testCount}: {r}\n')
                val1 = random.randint(lowVal, highVal)
                val2 = random.randint(lowVal, highVal)
                Generate2InputALUTest(val1, val2, testFunc(val1, val2))
                testCount += 1
    
    # finish off the test file with the following line and write
    lines.append('1 1 1 1')

    with open(f'{outputDir}/{outputFile}', 'w+') as f:
        f.writelines(lines)

    print(f'Lab program file generated for {testTitle}. Outputted to {outputDir}/{outputFile}')
    print(f'Generation runtime: {time.time() - startTime}')



bitwiseOperationsDict = dict(   {('AND',     (1, lambda x,y:  (x&y, 0))),
                                ('OR',      (2, lambda x,y:  (x|y, 0))),
                                ('NOR',     (3, lambda x,y:  (~(x|y), 0))),
                                ('XOR',     (4, lambda x,y:  (x^y, 0))),
                                ('NAND',    (5, lambda x,y:  (~(x&y), 0))),
                                ('XNOR',    (6, lambda x,y:  (~(x^y), 0))),
                                ('NOT',     (7, lambda x:    (~x, 0))),
                                ('SHL',     (8, MathUtility.SHL)),
                                ('SHR',     (9, MathUtility.SHR)),
                                ('ROTL',    (10, MathUtility.ROTL)),
                                ('ROTR',    (11, MathUtility.ROTR)),
                                ('ASHR',    (12, MathUtility.ASHR))})

integerOperationsDict = dict(   {('Negate',                      (16, MathUtility.IntegerNegate)),
                                ('Unsigned Addition',           (17, MathUtility.UnsignedAddition)),
                                ('Signed Addition',             (18, MathUtility.SignedAddition)),
                                ('Unsigned Subtraction',        (19, MathUtility.UnsignedSubtraction)),
                                ('Signed Subtraction',          (20, MathUtility.SignedSubtraction)),
                                ('Unsigned Multiplication',     (21, MathUtility.UnsignedMultiplication)),
                                ('Signed Multiplication',       (22, MathUtility.SignedMultiplication)),
                                ('Unsigned Integer Division',   (23, MathUtility.UnsignedIntegerDivision)),
                                ('Unsigned Integer Modulo',     (24, MathUtility.UnsignedIntegerModulo)),
                                ('Signed Integer Division',     (25, MathUtility.SignedIntegerDivision)),
                                ('Signed Integer Modulo',       (26, MathUtility.SignedIntegerModulo)),
                                ('Unsigned Integer to Float',   (27, MathUtility.UnsignedIntegerToFloat)),
                                ('Signed Integer to Float',     (28, MathUtility.SignedIntegerToFloat)),
                                ('Unsigned Integer to Double',  (29, MathUtility.UnsignedIntegerToDouble)),
                                ('Signed Integer to Double',    (30, MathUtility.SignedIntegerToDouble))})
 

# use all defaults
GenerateALUTest('Bitwise Operations', 'Bitwise Operations test.txt', bitwiseOperationsDict, ['NOT'])
GenerateALUTest('Integer Operations', 'Integer Operations test.txt', integerOperationsDict, ['Negate', 
                                                                                             'Unsigned Integer to Float', 
                                                                                             'Signed Integer to Float', 
                                                                                             'Unsigned Integer to Double', 
                                                                                             'Signed Integer to Double'])

print(f'Total runtime: {time.time() - globalStartTime}')
