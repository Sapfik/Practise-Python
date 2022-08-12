from googletrans import Translator
from google_trans_new import google_translator
# translator = google_translator()  
# translate_text = translator.translate('สวัสดีจีน',lang_tgt='en')  
# print(translate_text)

trans = Translator()
def to_ru(words):
    t = trans.translate(words, src = 'auto', dest='ru')
    return t.text

def to_de(words):
    t = trans.translate(words, src = 'auto', dest = 'de')
    return t.text
    
def to_pl(words):
    t = trans.translate(words, src = 'auto', dest= 'pl')
    return t.text

def to_es(words):
    t = trans.translate(words, src = 'auto', dest = 'es')
    return t.text

def to_ja(words):
    t = trans.translate(words, src = 'auto', dest='ja')
    return t.text

def to_fr(words):
    t = trans.translate(words, src = 'auto', dest = 'fr')
    return t.text
    

languages = ["Russian", "German", "Japanese", "Polish", "Spanish", "French"]

