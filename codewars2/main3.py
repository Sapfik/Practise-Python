

def sorted_nums(sentence):
    array = []
    for word in sentence:
        for k in list(range(1, 10)):
            if str(k) in word:
                array.append(k)
                
    return sorted(array)

def order(sentence):
    array = sorted_nums(sentence)
    last_array = []
    for i in array:
        for word in sentence.split():
            if str(i) in word:
                last_array.append(word)
    return ' '.join(last_array)

print(order('is2 Thi1s T4est 3a'))