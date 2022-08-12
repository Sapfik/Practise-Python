

def first_non_repeating_letter(string):
    string2 = string
    string = list(string)
    array = []
    word = ''
    for i in string:
        for j in string2:
            if i.lower() == j or i.upper() == j:
                array.append(i)
        if len(array) == 1:
            word = i
            break
        array.clear()
    
    return word

print(first_non_repeating_letter('hello world, eh?'))

##### Второе решение 

def first_non_repeating_letter(string):
    string_lower = string.lower()
    for i, letter in enumerate(string_lower):
        if string_lower.count(letter) == 1:
            return string[i]
            
    return ""