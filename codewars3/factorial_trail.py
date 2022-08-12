import re

def null_factorial(n):

    if int(n/5) < 1:
        return 0
    else:
        num = int(n/5) + int(null_factorial(n/5))
        return num
    
# def zeroes(base, number):
#   f = null_factorial(number)
#   for i in range(number): f *= i
#   m = re.search("0+$", str(f))
#   return m.end(0) - m.start(0) + 1

print(null_factorial(20, 1000))
