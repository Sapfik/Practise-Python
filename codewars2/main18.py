


def check_on_3x3(arr):
    num = 0
    my_array = list(range(1, 10))
    checklist = []
    for i in arr:
        checklist.extend(i[num:num+3])
    if sorted(checklist) == sorted(my_array):
        num += 3
        return True
    else:
        return False
    
def valid_solution(board):
    array_3x3 = []
    count = 0
    array = list(range(1, 10))
    for k, i in enumerate(board):
        if any(k == w for w in  [3, 6, 9]):
            
            while count <= 2:
                
                if check_on_3x3(array_3x3) == True:
                    count += 1
                else:
                    return False
            array_3x3 = []
            array_3x3.append(i)
            count = 0
        else:
            array_3x3.append(i)

    
    for i in board:
        if sorted(array) == sorted(i):
            continue
        else:
            return False
    return True
    
    
print(valid_solution([[5, 3, 4, 6, 7, 8, 9, 1, 2], 
                                   [6, 7, 2, 1, 9, 5, 3, 4, 8],
                                   [1, 9, 8, 3, 4, 2, 5, 6, 7],
                                   [8, 5, 9, 7, 6, 1, 4, 2, 3],
                                   [4, 2, 6, 8, 5, 3, 7, 9, 1],
                                   [7, 1, 3, 9, 2, 4, 8, 5, 6],
                                   [9, 6, 1, 5, 3, 7, 2, 8, 4],
                                   [2, 8, 7, 4, 1, 9, 6, 3, 5],
                                   [3, 4, 5, 2, 8, 6, 1, 7, 9]]))