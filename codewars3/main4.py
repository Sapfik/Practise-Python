
from numpy import array

array = []
array1 = [121, 144, 19, 161, 19, 144, 19, 131]
array2 = [11*11, 121*121, 144*144, 132*132, 161*161, 19*19, 144*144, 19*19]

def comp(array1, array2):
    for i in array1:
        for k in array2:
            if i == k ** 0.5:
                array.append(True)
                break
            else:
                array.append(False)
            
        if array[-1] == True:
            continue
        else:
            return False 

    return True

print(comp(array1, array2))
