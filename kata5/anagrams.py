from collections import Counter

def anagrams(word, words):
    return [i for i in words if Counter(word) == Counter(i)]

print(anagrams('racer', ['crazer', 'carer', 'racar', 'caers', 'racer']))