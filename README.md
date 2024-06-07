# Aplicações de Dados Ambientais

Este repositório contém duas aplicações distintas para acesso e visualização de dados ambientais. Uma aplicação foi desenvolvida utilizando Flask, e a outra com Streamlit. Ambas as aplicações utilizam a API OpenAQ para fornecer dados de qualidade do ar em tempo real.

## Aplicação Flask (`app.py`)

### Recursos

- **Integração com API**: Utiliza a API OpenAQ para obter dados de qualidade do ar em tempo real.
- **Manipulação de Dados**: Inclui tratamento robusto de erros e registros de eventos (logging) para interações com a API.
- **Parâmetros Ambientais**: Fornece dados como temperatura da água, salinidade, profundidade, pH e presença de espécies marinhas.

### Tecnologias Utilizadas

- Python
- Flask
- Requests
- Logging

## Aplicação Streamlit (`app_streamlit.py`)

### Recursos

- **Interface Visual Interativa**: Permite aos usuários selecionar um país e uma localização específica para acessar dados detalhados de qualidade do ar.
- **Visualização de Dados**: Apresenta um mapa interativo com a localização dos dados selecionados, utilizando a biblioteca Folium.

### Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Folium

## Instalação

Antes de executar as aplicações, instale as dependências necessárias. Execute o seguinte comando na raiz do diretório do projeto:

```
pip install -r requirements.txt
```

# Como Executar
## Flask
Para executar a aplicação Flask, utilize o comando:

```
python app.py
```

## Streamlit
Para iniciar a aplicação Streamlit, execute:

```
streamlit run app_streamlit.py
```


# Descrição do Dockerfile

- Imagem Base: Utiliza python:3.9-slim como a imagem base, que é uma versão reduzida da imagem oficial do Python, otimizada para aplicações que precisam de um ambiente Python minimalista.

- Diretório de Trabalho: Define /app como o diretório de trabalho dentro do contêiner. Todos os comandos subsequentes serão executados nesse diretório.

- Instalação de Dependências:

    - Cópia do requirements.txt: Copia o arquivo requirements.txt para o diretório de trabalho no contêiner.

    - Instalação de Dependências: Executa pip install --no-cache-dir -r requirements.txt para instalar as dependências do Python listadas no arquivo requirements.txt sem armazenar o cache, reduzindo o tamanho do contêiner.

- Cópia dos Códigos: Copia todo o código fonte restante para o diretório de trabalho no contêiner.

- Script de Inicialização:

    - Cópia e Permissões: Copia um script de inicialização start.sh para o diretório de trabalho e altera suas permissões para executável com chmod +x start.sh.
    - Execução da Aplicação: Define o comando CMD ["./start.sh"] para iniciar a aplicação quando o contêiner é executado.

- Porta: Expõe a porta 5000, que é a porta padrão usada pela aplicação Flask.

# Link do Pitch explicativo
https://youtu.be/bkOYn0f-2nE

# Modularização sugerida para melhorias futuras
```
├───app
│   ├───app.py
│   ├
│   ├───app_streamlit.py
│   ├───init_.py
│
├───API
│   ├───data
│   │   │   data.py
│   │   │
│   │   └───_pycache_
│   │           data.cpython-311.pyc
│   │
│   ├───routes
│   │   │   analise.py
│   │   │   api.py
│   │   │   _init_.py
│   │   │
│   │   └───_pycache_
│   │           analise.cpython-311.pyc
│   │           api.cpython-311.pyc
│   │           _init_.cpython-311.pyc
│   │
│   ├───services
│   │   │   openaq_service.py
│   │   │   _init_.py
│   │   │
│   │   └───_pycache_
│   │           openaq_service.cpython-311.pyc
│   │           _init_.cpython-311.pyc
│   │
│   └───utils
│           _init_.py
│
├───utils
│   │   _init_.py
│   │
│   ├───assets
│   │       fundo.jpg
│   │
│   ├───utils
│   │   │   data.py
│   │   │   deep_translate.py
│   │   │   image.py
│   │   │   openaq.py
│   │   │   _init_.py
│   │   │
│   │   └───_pycache_
│   │           data.cpython-311.pyc
│   │           deep_translate.cpython-311.pyc
│   │           image.cpython-311.pyc
│   │           openaq.cpython-311.pyc
│   │           _init_.cpython-311.pyc
│   │
│   └───_pycache_
│           _init_.cpython-311.pyc
│
└───_pycache_
        app.cpython-311.pyc
```