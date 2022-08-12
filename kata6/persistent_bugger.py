from functools import reduce
from operator import mul

def persistence(n):
    array = n
    count = 0
    for i in range(1, n):
        array = list(str(array))
        if len(array) > 1:
            array = reduce(mul, [int(i) for i in array])
            count += 1
        else:
            return count

print(persistence(999))