
# import itertools


# def sum_intervals(intervals):
#     new_intervals = []
#     array = []
#     count = 0
#     new_count = 0
#     for k, i in enumerate(intervals):
#         i = list(range(i[0], i[-1]+1))
        
#         for j in i:
#             if j not in new_intervals:
#                 new_intervals.append(j)
#         # for j in help_intervals:
#         #     j = lis
#         #     if i[-1] < j[-1] and i[0] in list(range(j[0], j[-1]+1)) and i != j:
#         #         itera = itertools.chain(i, j)
#     help_intervals = sorted(new_intervals[:])

#     for k, i in enumerate(sorted(new_intervals)):
#         try:
#             if help_intervals[count] - help_intervals[count+1] == 1 or help_intervals[count] - help_intervals[count+1] == -1:
#                 count += 1
#                 continue
#             else:
#                 array.append([help_intervals[0], help_intervals[count]])
#                 help_intervals = help_intervals[count+1:]
#                 count = 0
#         except:
#             array.append([help_intervals[0], help_intervals[count]])
#             count = 0
                
#     for i in array:
#         new_count += (abs(i[-1] - abs(i[0])))
#     return new_count
                
    
    

# print(sum_intervals([             [1,2],
#    [6, 10],
#    [11, 15]]))


def sum_of_intervals(intervals):
    result = set()
    for start, stop in intervals:
        for x in range(start, stop):
            result.add(x)
            
    return len(result)


print(sum_of_intervals([             [1,2],
   [6, 10],
   [11, 15]]))
