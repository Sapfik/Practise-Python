MORSE_CODE = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

def decode_morse(morse_code):
    global MORSE_CODE
    morse = ''
    array = []
    for k, i in enumerate(list(morse_code)):

        if ''.join(morse_code[k:k+3]) == '   ':
            array.append(morse)
            morse = ''
            array.append(' ') 
        elif i != ' ':
            morse += i
        else:
            array.append(morse)
            morse = ''
    array.append(morse)        
    array = [i for i in array if i != '']
    new_array = []
    for i in array:
        for k, v in MORSE_CODE.items():
            if v == i:
                new_array.append(k)
            elif i == ' ':
                new_array.append(' ')
                break
    return ''.join(new_array)


### SECOND SOLUTION
def decode_morse(morse_code):
    return ' '.join(''.join(MORSE_CODE[letter] for letter in word.split(' ')) for word in morse_code.strip().split('   '))



print(decode_morse('.... . -.--   .--- ..- -.. ....'))