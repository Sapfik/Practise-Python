

def array_diff(a, b):
    for i in b:
        while i in a:
            a.remove(i)
    return a

### SECOND SOLUTION
def array_diff(a, b):
    return [x for x in a if x not in b]

print(array_diff([1,2,2,3],[2, 3]))