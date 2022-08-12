import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

questionList = []

def getQuestions(tag, page):
    sql = sqlite3.connect('questions.sqlite')
    cursor = sql.cursor()
    
    url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={page}&pagesize=50'
    response = requests.get(url = url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    questions = soup.find_all('div', {'class' : 'question-summary'})

    for item in questions:

        title = item.find('a', {'class' : 'question-hyperlink'}).text
        link = 'https://stackoverflow.com' + item.find('a', {'class' : 'question-hyperlink'})['href']
        vote = int(item.find('span', {'class' : 'vote-count-post'}).text)
        date = item.find('span', {'class': 'relativetime'})['title']   #В title соджержится дата (она написанна не просто текстом) 
        
        cursor.execute(
            """
            INSERT INTO questions (title, link, votes, date) VALUES(?, ?, ?, ?)
            """, (title, link, vote, date)
        )
        sql.commit()
        
    return
               

getQuestions('python', 1)