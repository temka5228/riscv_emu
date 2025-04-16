def sextToInt(number, len_significant):
    mask = (1 << len_significant) - 1
    return number & mask

def intToSext(number, len_significant):
    sign = number >> len_significant
    if sign == 1:
        mask = (1 << len_significant) - 1
        signextended_number = - (((number & mask) - 1) ^ mask)
        return signextended_number
    else:
        return number
    
print(sextToInt(-10, 31), intToSext(-10, 31))