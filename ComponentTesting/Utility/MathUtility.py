import struct  # for float/double <--> integer conversions

# functions to help with performing operations on a list of bits


# get the first bits of an integer
# the math is identical for unsigned integers and integers encoded with 2's complement notation!
def IntToBits(num: int, numBits: int = 64) -> list:
    l = [0] * numBits

    for i in range(1, numBits+1):
        l[-i] = 1 if num % (2 ** i) != 0 else 0
        num -= num % (2 ** i)

        if (num == 0):
            break

    return l


# function to be safe about bounds
def UIntToBits(num: int, numBits: int = 64) -> list:
    # check that number falls within the bounds of the encoding
    if num < 0 or num > 2 ** numBits - 1:
        raise ValueError(f'{num} cannot be encoded as an unsigned {numBits}-bit integer.')

    return IntToBits(num, numBits)


# function to be safe about bounds
def SIntToBits(num: int, numBits: int = 64) -> list:
    # check that number falls within the bounds of the encoding
    if num < -2 ** (numBits-1) or num > 2 ** (numBits-1) - 1:
        raise ValueError(f'{num} cannot be encoded as a signed {numBits}-bit integer.')
    
    return IntToBits(num, numBits)


# convert bit list to unsigned integer
def BitsToUInt(bits: list) -> int:
    numBits = len(bits)
    num = 0

    for i in range(1, numBits+1):
        if bits[-i] == 1:
            num += 2 ** (i-1)
    
    return num


# convert bit list to signed integer
def BitsToSInt(bits: list) -> int:
    numBits = len(bits)
    num = 0

    if bits[0] == 1:
        num -= 2 ** (numBits-1)
    
    for i in range(1, numBits):
        if bits[-i] == 1:
            num += 2 ** (i-1)
    
    return num


# bit operations
def SHL(input1: int, input2: int) -> int:
    if abs(input2) >= 64:
        return (0, 0)
    
    l1 = SIntToBits(input1)
    ans = [0] * 64

    for i in range(64):
        if i - input2 >= 0 and i - input2 <= 63:
            ans[i-input2] = l1[i]
    
    return (BitsToSInt(ans), 0)


def SHR(input1: int, input2: int) -> int:
    return SHL(input1, -input2)


def ROTR(input1: int, input2: int) -> int:
    l1 = SIntToBits(input1)
    
    ans = [0] * 64
    for i in range(64):
        ans[(i + input2) % 64] = l1[i]
    
    return (BitsToSInt(ans), 0)


def ROTL(input1: int, input2: int) -> int:
    return ROTR(input1, -input2)


def ASHR(input1: int, input2: int) -> int:
    if input2 == 0:
        return (input1, 0)
    
    if input2 >= 64:
        if input1 >= 0:
            return (0, 0)
        else:
            return (-1, 0)
    
    if input2 <= -64:
        return (0, 0)
    
    l1 = SIntToBits(input1)

    if input2 < 0:
        ans = l1[-input2:] + [0] * -input2
        return (BitsToSInt(ans), 0)
    
    if input2 > 0:
        if input1 >= 0:
            ans = [0] * input2
        else:
            ans = [1] * input2
        
        ans += l1[:64-input2]
        return (BitsToSInt(ans), 0)



# integer operations - outputs are (output, flag byte)
# flag byte has the following bit layout from left to right:
# invalid opcode, carry, overflow, underflow, division by zero, sNaN,
# overflow flag, divideByZero flag)
def IntegerNegate(input1: int) -> tuple[int, int, int]:
    if input1 == -9223372036854775808:
        return (input1, 32)
    return (-input1, 0)


def UnsignedAddition(input1: int, input2: int) -> tuple[int, int, int]:
    # inputs are signed, we need to convert them to unsigned.
    i1 = BitsToUInt(SIntToBits(input1))
    i2 = BitsToUInt(SIntToBits(input2))
    ans = BitsToUInt(IntToBits(i1 + i2))  # keep only the first 64 bits
    output = BitsToSInt(UIntToBits(ans))  # convert to signed int, because thats how we have to check the output

    if (ans == i1 + i2):  # if these are not equal, then 64 bits is not enough to store the answer, and there is overflow!
        return (output, 0)
    return (output, 32)

def SignedAddition(input1: int, input2: int) -> tuple[int, int, int]:
    ans = BitsToSInt(IntToBits(input1 + input2))  # keep only the first 64 bits
    
    if (ans == input1 + input2):  # same idea as in UnsignedAddition()
        return (ans, 0)
    return (ans, 32)

def UnsignedSubtraction(input1: int, input2: int) -> tuple[int, int, int]:
    i1 = BitsToUInt(SIntToBits(input1))
    i2 = BitsToUInt(SIntToBits(input2))
    ans = BitsToUInt(IntToBits(i1 - i2))
    output = BitsToSInt(UIntToBits(ans))

    if (ans == i1 - i2):
        return (output, 0)
    return (output, 32)

def SignedSubtraction(input1: int, input2: int) -> tuple[int, int, int]:
    ans = BitsToSInt(IntToBits(input1 - input2))

    if (ans == input1 - input2):
        return (ans, 0)
    return (ans, 32)

def UnsignedMultiplication(input1: int, input2: int) -> tuple[int, int, int]:
    i1 = BitsToUInt(SIntToBits(input1))
    i2 = BitsToUInt(SIntToBits(input2))
    ans = BitsToUInt(IntToBits(i1 * i2))
    output = BitsToSInt(UIntToBits(ans))

    if (ans == i1 * i2):
        return (output, 0)
    return (output, 32)

def SignedMultiplication(input1: int, input2: int) -> tuple[int, int, int]:
    ans = BitsToSInt(IntToBits(input1 * input2))

    if (ans == input1 * input2):
        return (ans, 0)
    return (ans, 32)

def UnsignedIntegerDivision(input1: int, input2: int) -> tuple[int, int, int]:
    if (input2 == 0):
        return (0, 8)
    
    i1 = BitsToUInt(SIntToBits(input1))
    i2 = BitsToUInt(SIntToBits(input2))
    ans = BitsToUInt(IntToBits(i1 // i2))
    output = BitsToSInt(UIntToBits(ans))

    if (ans == i1 // i2):
        return (output, 0)
    return (output, 32)

def SignedIntegerDivision(input1: int, input2: int) -> tuple[int, int, int]:
    if (input2 == 0):
        return (0, 8)
    
    ans = BitsToSInt(IntToBits(input1 // input2))

    if (ans == input1 // input2):
        return (ans, 0)
    return (ans, 32)

def UnsignedIntegerModulo(input1: int, input2: int) -> tuple[int, int, int]:
    if (input2 == 0):
        return (0, 8)
    
    i1 = BitsToUInt(SIntToBits(input1))
    i2 = BitsToUInt(SIntToBits(input2))
    ans = BitsToUInt(IntToBits(i1 % i2))
    output = BitsToSInt(UIntToBits(ans))

    if (ans == i1 % i2):
        return (output, 0)
    return (output, 32)

def SignedIntegerModulo(input1: int, input2: int) -> tuple[int, int, int]:
    if (input2 == 0):
        return (0, 8)
    
    ans = BitsToSInt(IntToBits(input1 % input2))

    if (ans == input1 % input2):
        return (ans, 0)
    return (ans, 32)


# returns 64 bits, but only the last 32 bits will ever be nonzero
def floatToBits(input: float) -> list[int]:
    return [0] * 32 + SIntToBits(struct.unpack('>l', struct.pack('>f', input))[0])[32:]

def SignedIntegerToFloat(input1: int) -> tuple[int, int, int]:
    return (BitsToSInt(floatToBits(input1)), 0)

def UnsignedIntegerToFloat(input1: int) -> tuple[int, int, int]:
    return (BitsToSInt(floatToBits(BitsToUInt(SIntToBits(input1)))), 0)

def doubleToBits(input: float) -> list[int]:
    return SIntToBits(struct.unpack('>q', struct.pack('>d', input))[0])

def SignedIntegerToDouble(input1: int) -> tuple[int, int, int]:
    return (BitsToSInt(doubleToBits(input1)), 0)

def UnsignedIntegerToDouble(input1: int) -> tuple[int, int, int]:
    return (BitsToSInt(doubleToBits(BitsToUInt(SIntToBits(input1)))), 0)
