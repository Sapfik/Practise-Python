

# def split_list(alist, wanted_parts=1):
#     length = len(alist)
#     return  [alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
#              for i in range(wanted_parts) ]

# def sum_pairs(ints, s):
#     count = 0
#     array = split_list(ints, wanted_parts=2)
#     # num = array[0][count]
#     for char in array[0]:
#         for k, i in enumerate(array[0]):
#             try:
#                 if char + i == s:
#                     return [char, i]
#             except: 
#                 break
    
# def sum_pairs(ints, s):
#     count = 0
#     array = []
#     while count != len(ints) -1:
#         num = ints[count]
#         for i in ints:
#             if num + i == s:
#                 return [num, i]
#         count += 1

# print(sum_pairs([5, 13, -3], 10))



def sum_pairs(ints, s):
    prevMap = {}
    
    for i, n in enumerate(ints):
        diff = s - n
        if diff in prevMap:
            return [diff, n]
        prevMap[n] = i
    

print(sum_pairs([3, 2, 3, 4, 1, 0], 7))