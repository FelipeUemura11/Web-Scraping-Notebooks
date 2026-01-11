from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def scraper_notebooks():
    try:
        logger.info(" >> Iniciando o scraper de notebooks... << ")
        driver = webdriver.Chrome()
        
        driver.get("https://www.kabum.com.br/")

        wait = WebDriverWait(driver, 10)
        search_form = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        search_input = search_form.find_element(By.TAG_NAME, 'input')
        search_input.send_keys('notebook')
        search_input.send_keys(Keys.ENTER)

        time.sleep(5)

        driver.quit()

    except Exception as e:
        logger.error(f" >> Erro ao iniciar o scraper de notebooks: {e} << ")
        raise
