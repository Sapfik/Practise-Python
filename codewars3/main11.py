

def move_zeroes(array):
    for i in array:
        if i == 0:
            array.remove(i)
            array.append(0)
    return array

print(move_zeroes([9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]))