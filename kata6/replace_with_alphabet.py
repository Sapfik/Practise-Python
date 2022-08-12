import string

def alphabet_position(text):
    dic = {}
    for k, i in enumerate(list(string.ascii_lowercase)):
        dic[i] = k+1
    
    return ' '.join([str(dic.get(i)) for i in text.lower() if i.isalpha()])

print(alphabet_position("The sunset sets at twelve o' clock."))