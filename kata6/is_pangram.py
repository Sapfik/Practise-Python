import string

def is_pangram(s):
    array = [False if i not in s.lower() else True for i in string.ascii_lowercase ]
    return False if False in array else True


###SECOND SOLUTION
def is_pangram(s):
    return set(string.ascii_lowercase) <= set(s.lower())
    

print(is_pangram("The quick, brown fox umps over the lazy dog!"))