from bs4 import BeautifulSoup
import requests
from proxy_auth import proxies
import lxml

def get_data(url):
    data = ()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    req = requests.get(url=url, headers=headers, proxies=proxies)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    href = soup.find('div', class_='css-6f91y1').find('a', class_='css-1ej4hfo').get('href')
    name = soup.find('div', class_='css-6f91y1').find('a', class_='css-1ej4hfo').text
    data = (name, 'https://www.binance.com/'+href)
    return(str(data))

def write_file(data):
    with open("data.txt", "w") as file:
        file.write(data)

with open("data.txt", "r") as f:
    text = f.read()
