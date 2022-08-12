from collections import deque

def arrange(s):
    q = deque(s)
    return [q.pop() if 0<i%4<3 else q.popleft() for i in range(len(s))]

print(arrange([9, 7, -2, 8, 5,10,-3, 6, 5, 1]))
