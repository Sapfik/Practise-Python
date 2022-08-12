
import itertools

def permutations(string):
    stri = []
    array = []
    s = ''
    per = itertools.permutations(string)
    for val in per:
        for i in val:
            s += i
        # if s not in stri:
        stri.append(s)
        s = ''
    for k in stri:
        if k not in array:
            array.append(k)
    return array

print(permutations('aabb'))