

### FIRST SOLUTION
def unique_in_order(iterable):
    if len(iterable) != 0:
        res = [iterable[0]]
        iterable = list(iterable)
        for idx in range(1, len(iterable)):
            if iterable[idx-1] != iterable[idx]:
                res.append(iterable[idx])
            else:
                continue
        return res
    return []


### SECOND SOLUTION
def unique_in_order(iterable):
    if len(iterable) != 0:
        res = [iterable[0]]
        return res + [iterable[idx] for idx in range(1, len(list(iterable))) if iterable[idx-1] != iterable[idx]]
    else:
        return []


print(unique_in_order('AAAABBBCCDAABBB'))