import requests
from bs4 import BeautifulSoup
import pandas as pd

coin_algo_ids = ['162-etc-etchash','101-xmr-randomx']

for coin_algo in coin_algo_ids:
    url = f"https://whattomine.com/coins/{coin_algo}/gpus"

    response = requests.get(url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find_all('tr')[1:]: 
        cells = tr.find_all(['td', 'th'])
        row = [cell.text.strip() for cell in cells]
        if row:
            rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(f"../mining-gpus-{coin_algo}.csv", index=False, sep='|')
