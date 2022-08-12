import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency():

    url = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%BD&rlz=1C1SQJL_ruUA809UA809&oq=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+%D0%B2+%D0%B3%D1%80%D0%BD&aqs=chrome..69i57j0i10i433j0i512l4j0i10l4.4366j1j7&sourceid=chrome&ie=UTF-8'
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(',' , '.'))

    def get_currency_price(self):
        request = requests.get(url = self.url, headers= self.headers)
        soup = BeautifulSoup(request.content, 'lxml')

        convert = soup.findAll('span' , {'class' : 'DFlfde' , 'class' : 'SwHCTb' , "data-precision" : 2})  #второй и более рабочий способ
        # есть еще один способ (convert = soup.find('span' , class_ = 'DFlfde.SwHCTb'))  ты это писал, но почему оно не работает
        return convert[0].text

    def check_currency(self):
        currency  = float(self.get_currency_price().replace(',' , '.'))
        if currency >= self.current_converted_price +  self.difference:
            print('Course is going to up')
            self.send_email()
        elif currency <= self.current_converted_price - self.difference:
            print('Course is going to down')
            self.send_email()

        print('Course of 1 dollar: ' + str(currency))
        time.sleep(3)
        self.check_currency()

    def send_email(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('ilya.cheremisin.2018@gmail.com' , 'kcoltawdknvfavwr')

        subject = 'Exchange Rates'
        body = 'Course has been changed!'
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail  ( 
            'ilya.cheremisin.2016@gmail.com',   # От кого будет приходить сообщение
            'ilya.cheremisin.2018@gmail.com',   # Кому будет приходить сообщение 
            message  
        )

currency = Currency()
currency.check_currency()



 