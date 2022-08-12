


def solution (a_num):
    dict_out = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 
                10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 
                100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 
                1000: 'M'}
    r_num = ''
    for cnt in [1000, 100, 10, 1]:
        num = a_num % (cnt * 10) - a_num % cnt               
        if num in dict_out.keys():
            r_num += dict_out[num]
        else:
            if (1 * cnt) < num < (4 * cnt):
                r_num += dict_out[1 * cnt] * (num // cnt)
            elif (5 * cnt) < num < (9 * cnt):
                r_num += dict_out[5 * cnt] + dict_out[1 * cnt] * (num // cnt - 5)
    return r_num

print(solution(21))


#SECOND SOLUTION

vals = zip(('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'),
           (1000, 900, 500,  400, 100,   90,  50,   40,  10,    9,   5,    4,   1))

def solution(n):
    if n == 0: return ""
    return next(c + solution(n-v) for c,v in vals if v <= n)