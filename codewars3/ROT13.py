import codecs
import re
import string

def to_dic():
    dic = {}
    lower_array = list(string.ascii_lowercase)
    count = 1
    for i in lower_array[:13]:
        dic[i] = lower_array[count+12]
        count += 1

    count = 1
    upper_array = list(string.ascii_uppercase)
    for i in upper_array[:13]:
        dic[i] = upper_array[count+12]
        count += 1
    
    return dic


def rot13(message):

    dic = to_dic()
    array = []
    new_message = ''
    message = message.replace('\n', '\\.').replace('\t', '\\!').replace('\x0c', '\\?').replace('\x0b', '\\>').replace('\r', '\\<')
    for word in message.split():
        for i in word:
            for letter in dic:
                if letter == i:
                    new_message += i.replace(letter, dic[letter])
                elif dic[letter] == i:
                    new_message += i.replace(dic[letter], letter)
                elif i not in dic and i not in dic.values():
                    new_message += i
                    break
        if new_message == '':
            array.append(word)
        array.append(new_message) 
        new_message = ''   
    return ' '.join(array).replace('\\.', '\\n').replace('\\!', '\\t').replace('\\?', '\\x0c').replace('\\>', '\\x0b').replace('\\<', '\\r')
        

print(rot13("thl'\nf"))



### SECOND SOLUTION 
from codecs import encode
def rot13(message):
  return encode(message, 'rot13')

print(rot13("thl'\nf"))



### THIRD SOLUTION

def rot13(message):
    root13in = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    root13out = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    root13map = dict(zip(root13in, root13out))
    
    res = ''.join([root13map.get(s, s) for s in message])
    
    return res

print(rot13("thl'\nf"))

