

from itertools import permutations


def next_smaller(number):
    perm =  permutations(list(map(int, str(number))))
    # for i in list(perm):
    #     print(i)
    perm = list(perm)
    for i in perm:
        if i[0] == 0:
            i.
    return perm
    # res = [int(''.join(map(str, idx))) for idx in perm]
    # return res 

    # number = number.split()
    # perm = permutations(number)
    # for i in list(perm):
    #     print(i)
    # array = list(str(number))
    # new_array = array[:]
    # count = -1
    # for i in array:
    #     try:
    #         new_array[count-1] = array[count]
    #         new_array[count] = array[count-1]
    #         if int(''.join(new_array)) < number:
    #             return int(''.join(new_array))
    #         count -= 1
    #         new_array = array[:]
    #     except IndexError as ex:
    #         break
    
    # return -1 

print(next_smaller(907))