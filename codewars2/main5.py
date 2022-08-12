


def solution(number):
    array = list(range(1, number))
    val = 0
    for i in array:
        if any(i % w == 0 for w in [3, 5]):
            val += i

    return val

print(solution(41))


### 
def solution(number):
    return sum(x for x in range(number) if any(x % w == 0 for w in [3, 5]))

