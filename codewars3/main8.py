
def conversion_to_dictionary():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
    array = list(alphabet)
    dictory = {}
    for k, i in enumerate(array):
        dictory[i] = k+1
    return dictory


def high(sentence):
    dict_of_sum = {}
    array = conversion_to_dictionary()
    sentence = sentence.split()
    for word in sentence:
        suma = 0
        for i in word:
            for k in array:
                if k == i:
                    suma += array[k]
                    
        dict_of_sum[word] = suma

    
    max_val = max(dict_of_sum.values())
    for num in dict_of_sum:
        if max_val == dict_of_sum[num]:
            return num


print(high("what time are we climmmmmmmbing up the volcano"))