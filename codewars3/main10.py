

def generate_hashtag(s):
    array = s.split()
    hashtag = '#'
    s = s.replace(' ' , '')
    if len(s) == 0 or len(s) > 140:
        return False
    else:
        for word in array:
            word = word.capitalize()
            hashtag += word
        return hashtag
    

def generate_hashtag(sentence):
    hashtag = '#'
    
    for word in sentence.split():
        hashtag += word.capitalize()
    
    return False if len(sentence) == 0 or len(sentence) > 140 else hashtag 
    
    



print(generate_hashtag('Codewars'))