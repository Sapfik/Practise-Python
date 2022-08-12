

def ips_beetwen(start, end):
    num1 = 0
    num2 = 0
    array1 = start.split('.')
    array2 = end.split('.')
    count_ips = [256 ** 3, 256 ** 2, 256, 1]
    for k, i in enumerate(array1):
        num1 += int(i) * count_ips[k]
    
    for k,i in enumerate(array2):
        num2 += int(i) * count_ips[k]
        
    return num2 - num1

print(ips_beetwen("20.0.0.10", "20.0.1.0"))


### SECOND SOLUTION
def ips_between(start, end):
    a = sum([int(e)*256**(3-i) for i, e in enumerate(start.split('.'))])
    b = sum([int(e)*256**(3-i) for i, e in enumerate(end.split('.'))])
    return abs(a-b)