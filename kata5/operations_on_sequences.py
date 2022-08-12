

from itertools import pairwise


def solve(arr):
    count = 0
    result = 1
    new_result = 0
    seq = 0
    for k, i in pairwise(arr):
        if count % 2 == 0:
            result *= (k*k + i*i)
            count += 1
        else:
            count += 1
    count = 1
    while True:
        new_result = result - count ** 2
        seq = new_result**(1/2)
        if str(seq).split('.')[1] == '0':
            return [count ,int(seq)]
        count += 1
            

print(solve([3, 9, 8, 4, 6, 8, 7, 8, 4, 8, 5, 6, 6, 4, 4, 5]))