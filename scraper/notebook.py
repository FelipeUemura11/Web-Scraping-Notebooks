from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Scraper de navegação
def scraper_nav():
    try:
        logger.info(" >> Iniciando o scraper de notebooks... << ")
        driver = webdriver.Chrome()
        
        driver.get("https://www.kabum.com.br/")

        wait = WebDriverWait(driver, 10)
        search_form = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        search_input = search_form.find_element(By.TAG_NAME, 'input')
        search_input.send_keys('notebook')
        search_input.send_keys(Keys.ENTER)

        time.sleep(3)
        
        html = driver.page_source

        scraper_bs4(html)

        driver.close()

    except Exception as e:
        logger.error(f" >> Erro ao iniciar o scraper de notebooks: {e} << ")
        raise

# Scraper de extração de dados
def scraper_bs4(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        produtos = soup.find_all('article', class_='productCard')

        notebooks = []

        for produto in produtos:
            try:
                titulo_elemento = produto.find('span', class_='nameCard')
                titulo = titulo_elemento.get_text(strip=True) if titulo_elemento else 'Título não encontrado'

                preco_elemento = produto.find('span', class_='priceCard')
                preco = preco_elemento.get_text(strip=True) if preco_elemento else 'Preço não encontrado'
                
                if preco > 1000 and preco < 3000:
                    


                notebooks.append({
                    'titulo': titulo,
                    'preco': preco
                })

            except Exception as e:
                logger.warning(f" >> ERROR: Falha ao extrair dados de um produto: {e} <<")
                continue

        logger.info(f" >> Total de notebooks extraídos: {len(notebooks)} << ")

        

        return notebooks

    except Exception as e:
        logger.error(f" >> Erro ao iniciar o scraper de notebooks: {e} << ")
        raise
