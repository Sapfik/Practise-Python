# Initialize a list
# primes = []
# def is_primal(lst):
#     for possiblePrime in range(2, max(lst)):
        
#         # Assume number is prime until shown it is not. 
#         isPrime = True
#         for num in range(2, possiblePrime):
#             if possiblePrime % num == 0:
#                 isPrime = False
        
#         if isPrime:
#             primes.append(possiblePrime)
        
#     return primes
            
# print(is_primal([15, 21, 24, 30, 45]))



def is_palindrom(text):
    # return text.replace(' ', '').lower()[::-1]
    return True if text.replace(' ', '').lower() == text.replace(' ', '').lower()[::-1] else False

print(is_palindrom('А роза упала на лапу Азор'))
