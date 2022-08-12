
import math

def zeros(n):
    factorial = 1
    count = -1
    num = 0
    factorial = math.factorial(n)
    new_array = list(str(factorial))
    for char in new_array:
        if new_array[count] == '0':
            num += 1
            count -= 1
        else:
            break
    return num
            
print(zeros(1000))


