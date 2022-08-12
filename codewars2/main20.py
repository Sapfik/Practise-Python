

# def increment_string(string):
#     array = list(range(0, 10))
#     string = list(string)
#     second_string = string.copy()
#     last_string = ''
#     zeroes_array = []
#     count = -1
#     for i in string:
#         try:
#             if int(second_string[count]) in array:
#                 last_string = second_string[count] + last_string
#                 second_string.pop(-1)
#         except: 
#             if  list(last_string)[0] != '0':        
#                 second_string.append(str(int(last_string)+1)) if last_string != '' else second_string.append('1')
#                 return ''.join(second_string)
#             else:
#                 break
            
        
#     for k,i in enumerate(last_string):
#         if i != '0':
#             last_string = int(last_string[k:]) + 1
#             last_string = str(last_string)
#             if len(list(last_string[k:])) > len(zeroes_array):
#                 return '0' * len(zeroes_array) + last_string
#             break
#         else:
#             zeroes_array.append(0)
#     return ''.join(second_string) + str(last_string).zfill(len(zeroes_array)+1)        
#     # second_string.append(str(int(last_string)+1)) if last_string != '' else second_string.append('1')
#     # return ''.join(second_string)        
    
# print(increment_string('635x.Vj99M2HbFKkvB00'))



def increment_string(strng):

    # strip the decimals from the right
    stripped = strng.rstrip('1234567890')

    # get the part of strng that was stripped
    ints = strng[len(stripped):]

    if len(ints) == 0:
        return strng + '1'
    else:
        # find the length of ints
        length = len(ints)

        # add 1 to ints
        new_ints = 1 + int(ints)

        # pad new_ints with zeroes on the left
        new_ints = str(new_ints).zfill(length)

        return stripped + new_ints
    
print(increment_string('635x.Vj99M2HbFKkvB005757568858'))