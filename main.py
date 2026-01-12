import logging
from scraper.notebook import scraper_nav

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info(" >> Iniciando o navegador Chrome... << ")
        scraper_nav()
    except Exception as e:
        logger.error(f" >> Erro ao iniciar o navegador: {e} << ")
        raise

if __name__ == "__main__":
    main()