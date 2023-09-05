import requests

# URL da sua API
url = 'https://api.example.com/data.csv'

# Fazer a requisição GET para a API
response = requests.get(url)

# Verificar se a resposta foi bem-sucedida
response.raise_for_status()

# Caminho onde você deseja salvar o arquivo CSV
file_path = 'data.csv'

# Gravar o conteúdo da resposta em um arquivo CSV
with open(file_path, 'wb') as file:
    file.write(response.content)

print(f"CSV saved to {file_path}")