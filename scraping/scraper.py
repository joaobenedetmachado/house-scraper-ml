from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import csv
import os
from datetime import datetime

options = Options()
options.headless = True
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.binary_location = "/usr/bin/google-chrome-stable"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("iniciando scraper do OLX")
target = input('OLX link: ')
driver.get(target)
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
links = [a['href'] for a in soup.find_all('a', class_='olx-adcard__link')]
print(f"{len(links)} links de imóveis encontrados")

links_existentes = set()
csv_path = 'links/raw/raw.csv'

if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  #
                link = row[0] 
                links_existentes.add(link)
    print(f"já existentes no CSV: {len(links_existentes)}")
else:
    print("CSV vazio ou não existe - começando do zero")

links_novos = []
for link in links:
    if link not in links_existentes:
        links_novos.append(link)
    else:
        print(f"duplicado ignorado: {link}")

print(f"novos encontrados: {len(links_novos)}")

if links_novos:
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links_novos:
            writer.writerow([link])
    print(f"{len(links_novos)} novos links salvos no CSV")
else:
    print("nao tem link novo para salvar")

driver.quit()