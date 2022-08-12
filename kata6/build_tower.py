

def tower_builder(n):
    return [" " * (n - i - 1) + "*" * (2*i + 1) + " " * (n - i - 1) for i in range(n)]

### SECOND SOLUTION
def tower_builder(n_floors):
    res = []
    array = []
    count = 0
    for i in range(1, n_floors+1):
        res.append('*' * (i+count))
        count += 1
    
    last = res[-1]
    for k in res[:-1]:
        diff = len(last) - len(k)
        result = f"{' ' * (diff//2)}" + k + f"{' ' * (diff//2)}"
        array.append(result)
    array.append(last)
    return array
    
print(tower_builder(6))