import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def converter(preco_string):
    try:
        preco_clean = preco_string.replace('R$', '').replace('&nbsp;', '').strip()
        preco_clean = preco_clean.replace('.', '').replace(',', '.')
        return float(preco_clean)
    except (ValueError, AttributeError):
        return None

# Salva os notebooks em um arquivo JSON
def save_notebooks(notebooks):
    try:
        # Arquivo de notebooks JSON
        results_notebooks = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results_notebooks')
        os.makedirs(results_notebooks, exist_ok=True)
        name_arq = 'notebooks.json'
        arq = os.path.join(results_notebooks, name_arq)

        # Arquivo de notebooks repetidos JSON
        name_arq_repeted = 'repeted_notebooks.json'
        arq_repeted = os.path.join(results_notebooks, name_arq_repeted)

        exists = []
        if os.path.exists(arq):
            with open(arq, 'r', encoding='utf-8') as f:
                try:
                    exists = json.load(f) or []
                except json.JSONDecodeError:
                    exists = []
        
        merged_notebooks = exists + notebooks

        seen = set()
        output = []
        repeted = []
        
        for item in merged_notebooks:
            k = (item.get("titulo"), item.get("preco"), item.get("preco_num"))
            if k in seen:
                repeted.append(item)
                continue
            seen.add(k)
            output.append(item)

        with open(arq, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        with open(arq_repeted, 'w', encoding='utf-8') as f:
            json.dump(repeted, f, ensure_ascii=False, indent=2)

        logger.info(f" >> Notebooks salvos em: {arq} << ")
        logger.info(f" >> Total de notebooks salvos: {len(output)} << ")

    except Exception as e:
        logger.error(f" >> Erro ao salvar os notebooks: {e} << ")
        raise