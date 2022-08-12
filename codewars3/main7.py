
def find_outlier(integers):
    even_numbers = []
    odd_numbers = []
    for char in integers:
        if char % 2  == 0:
            even_numbers.append(char)
        else:
            odd_numbers.append(char)
        
    return even_numbers[-1] if len(even_numbers) == 1 else odd_numbers

print(find_outlier([160, 3, 1719, 19, 11, 13, -21]))


# def find_outlier(integers):
#     odds = [x for x in int if x%2!=0]
#     evens= [x for x in int if x%2==0]
#     return odds[0] if len(odds)<len(evens) else evens[0]