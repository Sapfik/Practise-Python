import requests
from bs4 import BeautifulSoup

fb_request = requests.get('https://finance.yahoo.com/quote/FB?p=FB')
soup = BeautifulSoup(fb_request.text, "html.parser")
fb_price = f"{soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')['value']}$"

tsla_request = requests.get(url = 'https://finance.yahoo.com/quote/TSLA?p=TSLA')
soup = BeautifulSoup(tsla_request.text, 'lxml')
tsla_price = f"{soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')['value']}$"

goog_request = requests.get(url = 'https://finance.yahoo.com/quote/GOOG?p=GOOG')
soup = BeautifulSoup(goog_request.text, 'lxml')
goog_price = f"{soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')['value']}$"

appl_request = requests.get(url = 'https://finance.yahoo.com/quote/AAPL?p=AAPL')
soup = BeautifulSoup(appl_request.text, 'lxml')
appl_price = f"{soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')['value']}$"

nvdia_request = requests.get(url = 'https://finance.yahoo.com/quote/NVDA?p=NVDA')
soup = BeautifulSoup(nvdia_request.text, 'lxml')
nvdia_price = f"{soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)')['value']}$"

stocks = {
	"Facebook": "FB",
	"Tesla": "TSLA",
	"Google": "GOOG",
	"Apple": "APL",
	"NVIDIA": "NVDA"
}