import random

def find_uniq (arr):
    return max(arr) if max(arr) != arr[random.randint(1, 2)] or max(arr) != arr[random.randint(1, 2)] else min(arr)

print(find_uniq([ 1, 1, 1, 2, 1, 2 ]))


### SECOND SOLUTION
def find_uniq(arr):
    a = sorted(arr)
    return a[0] if a[0] != a[1] else a[-1]