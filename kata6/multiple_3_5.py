

def solution(number):
    array = sum([i for i in range(0, number) if i % 3 == 0 or i % 5 == 0])
    return array if array > 0 else 0

print(solution(-200))