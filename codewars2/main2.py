

def sum_two_smallest_numbers(numbers):
    val = min(numbers)
    numbers.remove(val)
    return min(numbers) + val

print(sum_two_smallest_numbers([25, 42, 12, 18, 22]))


#SECOND SOLUTION
def sum_two_smallest_numbers(numbers):
    return sum(sorted(numbers)[:2])


print(sum_two_smallest_numbers([25, 42, 12, 18, 22]))