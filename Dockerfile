FROM python:3.12-slim

# Evita criação de arquivos .pyc e mantém logs imediatamente disponíveis
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Dependências necessárias para algumas bibliotecas Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia primeiro o requirements para aproveitar o cache do Docker
COPY requirements.txt .

# Atualiza o pip e instala as dependências
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

