# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do projeto para o diretório de trabalho
COPY . .

# Copie o script de inicialização para o diretório de trabalho
COPY start.sh .

# Dê permissão de execução ao script de inicialização
RUN chmod +x start.sh

# Exponha a porta que sua aplicação utiliza (se aplicável)
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["./start.sh"]
