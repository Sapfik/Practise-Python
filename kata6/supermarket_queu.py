

def queue_time(customers, n):
    l=[0]*n
    for i in customers:
        l[l.index(min(l))]+=i
    return max(l)
    
print(queue_time([6, 4, 42, 10, 42, 41, 29, 41, 36, 22, 36, 27, 40, 17, 28], 6))