import requests

# URL da sua API
url = 'https://api.example.com/data.csv'

# Fazer a requisição GET para a API com streaming habilitado
with requests.get(url, stream=True) as response:
    # Verificar se a resposta foi bem-sucedida
    response.raise_for_status()

    # Caminho onde você deseja salvar o arquivo CSV
    file_path = 'data.csv'

    # Gravar o conteúdo da resposta em um arquivo CSV em blocos
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192): 
            file.write(chunk)

print(f"CSV saved to {file_path}")