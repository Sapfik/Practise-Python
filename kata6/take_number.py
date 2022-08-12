


def dig_pow(n):
    return sum(int(x)**y for y,x in enumerate(str(n), 1))

def sum_dig_pow(a, b): 
    return [x for x in range(a,b + 1) if x == dig_pow(x)]


### SECOND SOLUTION
def split_nums(n):
    digits = []
    count = 1
    array = []
    while n > 0:
        digits.append((n % 10))
        n = (n - n % 10) // 10
    for i in digits[::-1]:
        array.append(i**count)
        count += 1
    return array


def sum_dig_pow(a, b):
    return [i for i in range(a, b+1) if i == sum(split_nums(i))]
        

# print(split_nums(89))
print(sum_dig_pow(90, 100))