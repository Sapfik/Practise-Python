import math

#Первое решение
def is_square (n):
    if n > 0:
        s = str(math.sqrt(n))
        is_square = s.split('.')[1]
        first_num = s.split('.')[0]
        if is_square == '0' or first_num == '0':
            return True
        else:
            return False
    else: 
        return False
    

#Второе решение
def is_square (n):
    return n >= 0 and (n**0.5) % 1 == 0

