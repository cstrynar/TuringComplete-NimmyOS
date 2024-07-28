# functions to help with performing operations on a list of bits


def UIntToBits(num: int, numBits: int = 64) -> list:
    l = [0] * numBits

    for i in range(1, numBits+1):
        l[-i] = 1 if num % (2 ** i) != 0 else 0
        num -= num % (2 ** i)

        if (num == 0):
            break

    return l

print(UIntToBits(123987980132790))

def BitsToInt_64(bits: list) -> int:
    pass