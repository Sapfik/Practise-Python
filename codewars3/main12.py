
import re
from turtle import right

def valid_parentheses(string):
    sentence = list(string)
    left_brackets = []
    right_brackets = []
    array = []
    
    count = 0
    for char in sentence:
        if char == '(':
            left_brackets.append('(')
            array.append(char)
        elif char == ')':
            right_brackets.append(char)
            array.append(char)
    
    array = ''.join(array)
    array = array.replace('()', '')
    array = array.replace('()', '')
    if ')(' in array or array == '(' or array == ')' or '))' in array or '((' in array:
        return False
    else:
        return True
            

print(valid_parentheses("kpw(qre(jeew()zaoaj"))


###################################

def valid_parentheses(string):
    cnt = 0
    for char in string:
        if char == '(': cnt += 1
        if char == ')': cnt -= 1
        if cnt < 0: return False
    return True if cnt == 0 else False