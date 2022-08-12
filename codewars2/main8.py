



def expanded_form(num):
    array = list(str(num)[1:])
    example = ''
    n = []
    last_array = []
    for k, i in enumerate(str(num)):
        if  i != '0':
            i += '0' * len(array)
            try:
                array.pop(0)
            except:
                n.append(i)
                break
        else:
            try:
                array.pop(0)
            except:
                break
        
        n.append(i)
        example = ''

    for j in n:
        if j != '0':
            last_array.append(j)
    return ' + '.join(last_array)

print(expanded_form(9000000))



### SECOND SOLUTION

def expanded_form(num):
    return ' + '.join([x+'0'*i for i,x in enumerate(str(num)[::-1]) if x != '0'][::-1])