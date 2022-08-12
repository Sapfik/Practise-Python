

from collections import Counter    # Функция Couner для того, чтобы можно было посчитать все значения хеш-таблицы, которые имеют одни и те же ключи в списке 

def scramble(s1, s2):
    dict1 = Counter(s1)
    dict2 = Counter(s2)
    for key in dict2:
        if dict2[key] > dict1[key]:
            return False
    return True
    

print(scramble('katas', 'steak'))


def scramble(s1,s2):
    for c in set(s2):
        if s1.count(c) < s2.count(c):
            return False
    return True