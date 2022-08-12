
from itertools import pairwise

def find(seq):
    seq = sorted(seq)
    count = (seq[-1] - seq[0]) // len(seq)
    return int(''.join([str(k + count) for k,i in pairwise(seq) if i - k != count]))

print(find([3, 9, 1, 11, 13, 5]))