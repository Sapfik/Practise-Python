

def parts_sums(ls):
    array = [sum(ls[k:]) for k,i in enumerate(ls)]
    array.append(0)
    return list(array)

print(parts_sums([0, 1, 3, 6, 10]))