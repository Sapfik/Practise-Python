

def chain_sum(number):
    result = number
    def wrapper(number2=None):
        nonlocal result
        if number2 is None:
            return result       
        result += number2
        return wrapper
    return wrapper

print(chain_sum(5)())
print(chain_sum(5)(12)())
print(chain_sum(5)(95)(-10)())


### SECOND SOLUTION

class chain_sum(int):
    def __call__(self, additive = 0):
        return chain_sum(self+additive)

print(chain_sum(5))
print(chain_sum(5)(12))
print(chain_sum(5)(95)(-10))