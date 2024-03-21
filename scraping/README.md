# scraping

```bash
# Cria um ambiente virtual
python -m venv venv

# Acessa o ambiente virtual (Unix)
source venv/bin/activate

# Acessa o ambiente virtual (Windows)
.\venv\Scripts\activate

# Atualiza o gerenciador de pacotes do Python
python -m pip install --upgrade --no-cache-dir pip

# Instala as dependências necessárias
pip install -r requirements.txt

# Realiza o scraping dos pesquisadores
scrapy crawl pesquisadores

# Realiza o scraping de cada pesquisador
scrapy crawl pesquisador
```
