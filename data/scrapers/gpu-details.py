import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import random
from time import sleep

DETAILS_FILE = '../gpu-details.csv'
made_changes = False

with open('../proxies.txt', 'r', encoding='utf-8') as f:
    proxy_list = f.readlines()

proxy_index = 0
proxy = proxy_list[proxy_index]

base_url = 'https://www.techpowerup.com' 
options = uc.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_argument(f'--proxy-server={proxy}')
prefs = {"profile.managed_default_content_settings.images": 2, "javascript.enabled": False}
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(headless=True)

gpus_df = pd.read_csv(DETAILS_FILE, sep='|')
for index, row in gpus_df.iterrows():
    print(f'Processing index: {index}')
    if(index%10 == 0 and made_changes):
        print('Saving data')
        print(f'Column preview: {gpus_df.columns}')
        gpus_df.to_csv(DETAILS_FILE, sep='|', index=False)

    if(row.notna().sum() > 2):
        continue

    try:
        driver.get(f"{base_url}{row['Product Link']}")
    except:
        with open('../proxies.txt', 'w', encoding='utf-8') as f:
            f.writelines(proxy_list[1:])
        print('PROXY HAS BEEN USED UP X')
        exit(-1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    details = soup.select('div.sectioncontainer section div dl')
    if(len(details) == 0):
        with open('../proxies.txt', 'w', encoding='utf-8') as f:
            f.writelines(proxy_list[1:])
        print('PROXY HAS BEEN USED UP')
        exit(-1)

    for detail in details:
        spec_name = detail.find('dt')
        if(spec_name):
            spec_name = spec_name.text.strip()
            spec_value = detail.find('dd').text.strip()
            gpus_df.at[index, spec_name] = spec_value
            made_changes = True

    sleep(random.randint(5, 12))