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


def SHL(input1: int, input2: int) -> int:
    if abs(input2) >= 64:
        return 0
    
    l1 = SIntToBits(input1)
    ans = [0] * 64

    for i in range(64):
        if i - input2 >= 0 and i - input2 <= 63:
            ans[i-input2] = l1[i]
    
    return BitsToSInt(ans)


def SHR(input1: int, input2: int) -> int:
    return SHL(input1, -input2)


def ROTR(input1: int, input2: int) -> int:
    l1 = SIntToBits(input1)
    
    ans = [0] * 64
    for i in range(64):
        ans[(i + input2) % 64] = l1[i]
    
    return BitsToSInt(ans)


def ROTL(input1: int, input2: int) -> int:
    return ROTR(input1, -input2)


def ASHR(input1: int, input2: int) -> int:
    if input2 == 0:
        return input1
    
    if input2 >= 64:
        if input1 >= 0:
            return 0
        else:
            return -1
    
    if input2 <= -64:
        return 0
    
    l1 = SIntToBits(input1)

    if input2 < 0:
        ans = l1[-input2:] + [0] * -input2
        return BitsToSInt(ans)
    
    if input2 > 0:
        if input1 >= 0:
            ans = [0] * input2
        else:
            ans = [1] * input2
        
        ans += l1[:64-input2]
        return BitsToSInt(ans)
