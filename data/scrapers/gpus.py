import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import random
from time import sleep

options = uc.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
prefs = {"profile.managed_default_content_settings.images": 2, "javascript.enabled": False}
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(headless=True)

data = []
for gpu_brand in ['AMD', 'NVIDIA']:
    for year in range(2010, 2026):
        driver.get(f"https://www.techpowerup.com/gpu-specs/?f=mfgr_{gpu_brand}~year_{year}")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        rows = soup.select('table.items-desktop-table tbody tr')

        for row in rows:
            product_cell = row.find('td', class_=f'vendor-{gpu_brand}')
            if product_cell:
                link_tag = product_cell.find('a')
                product_name = link_tag.text.strip()
                product_url = link_tag['href']
                data.append({
                    'Product Name': product_name,
                    'Product Link': product_url
                })
        sleep(1)

df = pd.DataFrame(data)
df.to_csv('../gpus.csv', sep='|', index=False)
print(df)