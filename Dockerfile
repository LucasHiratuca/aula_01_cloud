# Usa uma imagem oficial do Python levinha como base
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro (otimização de cache do Docker)
COPY requirements.txt .

# Instala as bibliotecas que o seu projeto precisa
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu projeto para dentro do container
COPY . .

# Expõe a porta 8217 (a mesma configurada no app.py)
EXPOSE 8217

# O comando que o Portainer vai executar para ligar o servidor
CMD ["python", "app.py"]
