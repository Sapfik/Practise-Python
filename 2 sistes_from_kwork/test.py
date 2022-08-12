import re
text = 'https://truck.av.by/mercedes-benz/actros/100263425'

# text = re.split('\W+', text)
# new_text = text.strip(',')[:-1]
print(text.split("/")[-1])
