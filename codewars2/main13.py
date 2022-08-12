


from itertools import combinations

def choose_best_sum(t, k, ls):

    array = []
    for char in list(combinations((ls), k)):
        if sum(char) <= t:
            array.append(sum(char))
        else:
            continue
    return max(array) if len(array) > 0 else None
                

print(choose_best_sum(430, 5, ls = [100, 76, 56, 44, 89, 73, 68, 56, 64, 123, 2333, 144, 50, 132, 123, 34, 89]))


### SECOND SOLUTION

def choose_best_sum(t, k, ls):
    try: 
        return max(sum(i) for i in combinations(ls,k) if sum(i)<=t)
    except:
        return None





