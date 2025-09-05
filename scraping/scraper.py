from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
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

print("Iniciando scraper do OLX")

data = {
    'nome': 'h2',
    'preco': '.olx-adcard__price',
    'nquartos': 'section.olx-adcard > div > div > div > div > div:nth-child(1)',
    'nbanheiros': 'section.olx-adcard > div > div > div > div > div:nth-child(4)',
    'ngaragem': 'section.olx-adcard > div > div > div > div > div:nth-child(3)',
    'area': 'section.olx-adcard > div > div > div > div > div:nth-child(2)'
}

try:
    target = input('OLX link: ')
    driver.get(target)
    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    cards = soup.find_all('section', class_='olx-adcard')
    
    print(f"{len(cards)} encontrados")
    
    links_existentes = set()
    csv_path = 'data/raw/raw.csv'
    
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  
            for row in reader:
                if row and len(row) > 0:
                    links_existentes.add(row[0])
        print(f"{len(links_existentes)} links antes processados")
    else:
        print("comecando do zero")
    
    file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['link', 'nome', 'preco', 'nquartos', 'nbanheiros', 'ngaragem', 'area', 'data_scraping']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        novos_processados = 0
        
        for i, card in enumerate(cards):
            try:
                # link
                link_elem = card.find('a', class_='olx-adcard__link')
                if not link_elem:
                    continue
                    
                href = link_elem.get('href')
                if not href:
                    continue
                    
                if href.startswith('/'): 
                    link = 'https://olx.com.br' + href
                else:
                    link = href
                
                if link in links_existentes:
                    continue
                
                print(f"Processando {i+1}/{len(cards)}")
                
                dados = {
                    'link': link,
                    'nome': '',
                    'preco': '',
                    'nquartos': '',
                    'nbanheiros': '',
                    'ngaragem': '',
                    'area': '',
                    'data_scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                nome_elem = card.select_one(data['nome'])
                if nome_elem:
                    dados['nome'] = nome_elem.get_text(strip=True)
                
                preco_elem = card.select_one(data['preco'])
                if preco_elem:
                    dados['preco'] = preco_elem.get_text(strip=True)
                
                quartos_elem = card.select_one(data['nquartos'])
                if quartos_elem:
                    dados['nquartos'] = quartos_elem.get_text(strip=True)
                
                area_elem = card.select_one(data['area'])
                if area_elem:
                    dados['area'] = area_elem.get_text(strip=True)
                
                garagem_elem = card.select_one(data['ngaragem'])
                if garagem_elem:
                    dados['ngaragem'] = garagem_elem.get_text(strip=True)
                
                banheiros_elem = card.select_one(data['nbanheiros'])
                if banheiros_elem:
                    dados['nbanheiros'] = banheiros_elem.get_text(strip=True)
                
                # ordem especificada
                writer.writerow(dados)
                links_existentes.add(link)
                novos_processados += 1
                
                
            except Exception as e:
                print(f"erro no card {i+1}: {str(e)}")
                continue
    
    print(f"\nconcluido")
    print(f"Novos processados: {novos_processados}")

except Exception as e:
    print(f"Erro geral: {str(e)}")

finally:
    driver.quit()
    print("Driver fechado")