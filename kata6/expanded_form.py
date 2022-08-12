


### SECOND SOLUTION 
def expanded_form(num):
    integer_part, fractional_part = str(num).split('.')

    result = [str(int(num) * (10 ** i)) for i, num in enumerate(integer_part[::-1]) if num != '0'][::-1]
    result += [str(num) + '/' + str(10 ** (i + 1)) for i, num in enumerate(fractional_part) if num != '0']

    return ' + '.join(result)




def expanded_form(num):
    num = str(num).split('.')
    string = ''
    count = 10
    for k, number in enumerate(str(num[0])):
        if number != '0':
            string += f"{number}" + "0" * len(num[0][k+1:]) + ' + '
        
    for k, number in enumerate(str(num[1])):
        if number != '0':
            string += f"{number}/{count} + "
        count *= 10
        
    return string[0:-3]
    
    
   

print(expanded_form(709.304))