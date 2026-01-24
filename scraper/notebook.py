from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.functions import converter, save_notebooks
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

        try:
            logger.info(" >> Buscando Mais avaliados << ")
            # Busca o botão de ordenação (Mais procurados)
            sort_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[self::button or self::div][contains(., 'Mais procurados')]")
            ))
            sort_button.click()

            # Busca a opção de ordenação (Mais avaliações)
            opt = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[self::button or self::div][contains(., 'Mais avaliações')]")
            ))
            opt.click()

            wait.until(lambda d: "Mais avaliados" in d.page_source)
            
        html2 = driver.page_source 

        scraper_bs4(html2)

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
                preco_string = preco_elemento.get_text(strip=True) if preco_elemento else 'Preço não encontrado'
                
                preco_num = converter(preco_string)

                
                if preco_num is not None and preco_num > 1000 and preco_num < 3000:
                    notebooks.append({
                        'titulo': titulo,
                        'preco': preco_string,
                        'preco_num': preco_num
                    })

            except Exception as e:
                logger.warning(f" >> ERROR: Falha ao extrair dados de um produto: {e} <<")
                continue

        logger.info(f" >> Total de notebooks extraídos(R$1000-R$3000): {len(notebooks)} << ")

        if notebooks:
            save_notebooks(notebooks)
        else:
            logger.warning(f" >> Nenhum notebook encontrado(R$1000-R$3000) << ")

        return notebooks

    except Exception as e:
        logger.error(f" >> Erro ao iniciar o scraper de notebooks: {e} << ")
        raise
