

                                                ######## FIRST SOLUTION #########

def rgb(r, g, b):
    array = []
    code= ''
    s = ''
    h = '0123456789ABCDEF'
    array.append(r)
    array.append(g)
    array.append(b)
    for color in array:
        if color > 0 and color <= 9:
            while color > 0:
                s = '0'
                s = s + h[color % 16]
                color = color // 16              
            code += s
            s = ''
        elif color <= 0:
            code += '00'
        elif color > 255:
            code += 'FF'
        elif color > 0:
            while color > 0:
                s = h[color % 16] + s
                color = color // 16
            code += s
            s =''

                 
    return code
    

print(rgb(-64 ,252 ,143))

                                                ###### SECOND SOLUTION #########


def rgb(r, g, b):
    def get_hex(s):
        if s > 255: s = 255
        if s < 0: s = 0
        return hex(s)[2:].upper() if len(hex(s)[:2]) > 1 else "0" + hex(s)[:2]
        # hex - это встроенная функция в Пайтон, которая преобразует обычное число в шестнадцетеричную систему
        # [2:] - этот срез нужен для того, чтобы обрезать дебаф hex() (а именно в начале пишется 0X)
    return get_hex(r) + get_hex(g) + get_hex(b)

print(rgb(255, 9, -12))