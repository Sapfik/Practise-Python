presses_dict = {1}

def presses(phrase):
    result = 0
    keypad = {
        1:(1, "A", "D", 'G', 'J', 'M', 'P', "T", 'W', '*', '#', ' '),
        2:("B", "E", 'H', 'K', 'N', 'Q', "U", 'X', 0),
        3:("C", "F", 'I', 'L', 'O', 'R', "V", 'Y'),
        4:(2, 3, 4, 5, 6, 'S', 8, 'Z'),
        5:(7,9)  
    }
    phrase = phrase.upper()
    for i in phrase:
        for j in keypad:
            if i in keypad[j]:
                result += j
                
    return result

print(presses("WHERE DO U WANT 2 MEET L8R"))