import re
import requests
from bs4 import BeautifulSoup

xmr_request = requests.get(url = 'https://www.coingecko.com/en/coins/monero')
soup = BeautifulSoup(xmr_request.text, 'lxml')
# raw_xmr = soup.find_all('span', {'class': 'no-wrap'})[0].find_all(text=True, recursive=True)
# xmr_price = ''.join([str(elem) for elem in raw_xmr]) 
xmr_price = soup.find('span', {'class': 'no-wrap'}).text.strip()


btc_request = requests.get(url = 'https://api.coinbase.com/v2/prices/BTC-USD/spot')    #В url указываем ссылку на апи 
btc_data = btc_request.json()
btc_price = f"{btc_data['data']['amount']}$"

eth_request = requests.get(url = 'https://api.coinbase.com/v2/prices/ETH-USD/spot')
eth_data = eth_request.json()
eth_price = f"{eth_data['data']['amount']}$"

atom_request = requests.get(url = 'https://api.coinbase.com/v2/prices/ATOM-USD/spot')
atom_data = atom_request.json()
atom_price = f"{atom_data['data']['amount']}$"

solana_request = requests.get(url = 'https://api.coinbase.com/v2/prices/SOL-USD/spot')
solana_data = solana_request.json()
solana_price = f"{solana_data['data']['amount']}$"

coins = {
	"Bitcoin(BTC)": "BTC",
	"Ethereum(ETH)": "ETH",
    "Atom(ATOM)" : "ATOM",
    "Solana(SOL)" : "SOL",
	"Monero(XMR)": "XMR"
}