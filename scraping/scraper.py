from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://www.olx.com.br/imoveis/venda/casas/estado-sc/florianopolis-e-regiao/outras-cidades/criciuma")

time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

links = [a['href'] for a in soup.find_all('a', class_='olx-adcard__link')]
print(links)

driver.quit()

for i in links:
    driver.get(i)
