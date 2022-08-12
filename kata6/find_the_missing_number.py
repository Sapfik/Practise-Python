from itertools import pairwise

def find_missing(sequence):
    count = (sequence[-1] - sequence[0]) // len(sequence)
    return int(''.join([str(k + count) for k, i in pairwise(sequence) if i - k != count]))

print(find_missing([1, 2, 3, 4, 6, 7, 8, 9]))