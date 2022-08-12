

def is_prime(num):
    array = list(range(1, num+1))
    last_array = []
    for b in array:
        if num % b == 0 and b > 0:
             last_array.append(b)
    return True if len(last_array) == 2 else False
    
print(is_prime(-100))