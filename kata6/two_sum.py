from itertools import combinations

def two_sum(numbers, target):
    array = []
    for i in combinations(numbers, 2):
        if sum(i) == target:
            array = [numbers.index(i[0]), numbers.index(i[1])]
            if array[0] == array[1]:
                numbers.pop(array[0])
                return [array[0], numbers.index(i[1])+1]
            return [numbers.index(i[0]), numbers.index(i[1])]
        
        
### SECOND SOLUTION 
def two_sum(nums, t):
    for i, x in enumerate(nums):
        for j, y in enumerate(nums):
            if i != j and x + y == t:
                return [i, j]

print(two_sum([2,2,3], 4))