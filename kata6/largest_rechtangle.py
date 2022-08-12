

from itertools import pairwise


def lergest_rect(histogram):
    count = 0
    help_count = 0
    array = []
    
    for k,i in pairwise(histogram):
        print('*' * k)
        if k == i:
            array.append(k)
        if k < i:
            array.append(k)
        if k > i:
            array = []
            
    return array

print(lergest_rect([9, 7, 5, 4, 2, 5, 6, 7, 7, 5, 7, 6, 4, 4, 3, 2]))