

def pig_it(text):
    array = []
    for i in text.split():
        if i.isalpha():
            array.append(f"{i[1:]+i[0]}ay")
        else:
            array.append(i)
    return ' '.join(array)


### SECOND SOLUTION
def pig_it(text):
    lst = text.split()
    return ' '.join( [word[1:] + word[:1] + 'ay' if word.isalpha() else word for word in lst])
    

print(pig_it("Hello world !"))