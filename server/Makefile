# Makefile para rodar o app Python

# Nome do script principal
APP_FILE=app/main.py

# Ambiente Python (opcional)
PYTHON=python

.PHONY: start install lint clean

start:
	@echo "Iniciando aplicação com watch..."
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 333

install:
	@echo "Instalando dependências..."
	pip install -r requirements.txt

