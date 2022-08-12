

def find_it(seq):
    dic = {}
    for i in seq:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    
    for char in dic:
        if dic[char] % 2 != 0:
            return char
        else:
            pass
    

print(find_it([1,1,2,-2,5,2,4,4,-1,-2,5]))


### SECOND SOLUTION
def find_it(seq):
    return [x for x in seq if seq.count(x) % 2][0]

print(find_it([1,1,2,-2,5,2,4,4,-1,-2,5]))