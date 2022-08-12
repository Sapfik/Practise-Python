

from itertools import pairwise


def productFib(prod):
    array = [0, 1]
    for i in range(0, prod):
        if array[-1] > prod:
            break
        else:
            array.append(array[i]+array[i+1])
    
    for k, i in pairwise(array):
        if k*i > prod:
            return [k, i, False]
        if k*i == prod:
            return [k, i, True]

print(productFib(5895))