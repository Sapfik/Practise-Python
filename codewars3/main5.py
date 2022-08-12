

def solution (s):
    my_array = []
    array = list(s)
    count = 0
    c = ''
    for i in array:
        if i == ' ':
            i = '_'
        c = c + i
        count += 1
        
        if count >= 2:
            my_array.append(c)
            c = ''
            count = 0
    
    if c != '':
        c += '_'
        my_array.append(c)        
        
    return my_array


print(solution("ab c"))