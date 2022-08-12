# url ='https://www.securitylab.ru/news/525940.php'

# article_id = url.split('/')[-1]
# article_id = article_id[:-4]
# print(article_id)

import json

with open ('news_dict.json', encoding='utf-8') as file:
    news_dict = json.load(file)

search = "525951"
if search in news_dict:
    print('Этот элемент есть в словаре')
else:
    print('Этого элемента нету в словаре')