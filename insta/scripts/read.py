import json

with open('./users.json', 'r') as arquivo:
    dados = json.load(arquivo)

for item in dados:
    print(item['ID'])
