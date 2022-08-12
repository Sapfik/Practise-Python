from collections import Counter

def duplicate_count(text):
    return len([1 for i in Counter(text.lower()) if Counter(text.lower())[i] > 1])

print(duplicate_count('aabbcde'))