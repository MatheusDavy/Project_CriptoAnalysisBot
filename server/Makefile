# Makefile para rodar o app Python

# Nome do script principal
APP_FILE=app.py

# Ambiente Python (opcional)
PYTHON=python

.PHONY: start install lint clean

start:
	@echo "Iniciando aplicação com watch..."
	nodemon --exec $(PYTHON) $(APP_FILE)

install:
	@echo "Instalando dependências..."
	pip install -r requirements.txt

lint:
	@echo "Verificando estilo do código com flake8..."
	flake8 .

clean:
	@echo "Removendo arquivos __pycache__..."
	find . -type d -name "__pycache__" -exec rm -r {} +
