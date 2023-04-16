import requests
from datetime import date, timedelta
import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API e a URL base da API da Amadeus das variáveis de ambiente
API_ACCESS_TOKEN = os.getenv("AMADEUS_API_ACCESS_TOKEN")
BASE_URL = os.getenv("AMADEUS_API_BASE_URL")

# Calcula a data de 3 anos atrás a partir da data atual
hoje = date.today()
tres_anos_atras = hoje - timedelta(days=3 * 365)

# Parâmetros da busca de voos
params = {
    "originLocationCode": "GRU",  # Aeroporto de São Paulo
    "destinationLocationCode": "LIM",  # Aeroporto de Lima
    "departureDate": "2023-10-02",
    "adults": 1,
    "currencyCode": "BRL",
    "max": 10,  # Número máximo de resultados
}

# Faça a chamada à API da Amadeus usando a biblioteca 'requests'
response = requests.get(
    BASE_URL,
    params=params,
    headers={
        "Authorization": f"Bearer {API_ACCESS_TOKEN}",
    },
)

# Verifique se a resposta foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    # Extraia os dados de preços de voos do JSON de resposta
    # Exemplo de extração de preços:
    for offer in data["data"]:
        price = offer["price"]["grandTotal"]
        print(f"Preço R$: {price}")
    # print(f"Conteúdo da chamada da API: {response.text}")
else:
    print(f"Erro na chamada da API: {response.status_code} - {response.text}")
