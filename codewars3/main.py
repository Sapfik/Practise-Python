import re

def to_camel_case (text):
    last_word = ""
    count = 0
    changed_word =re.split(r"[-_]", text)

    for i in changed_word:
        try:
            if count == 0:
                prelast_word = changed_word[count]
            else:
                prelast_word = changed_word[count].capitalize()

            count += 1
            last_word += prelast_word
        except:
            break
        
    return last_word

print(to_camel_case('the-stealth-warrior'))
    
    


    
    
    
    