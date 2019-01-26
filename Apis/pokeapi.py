import requests

poke = input("Nome: ")
url = "https://pokeapi.co/api/v2/pokemon/%s" %poke

response = requests.get(url).json()
games = ""

for i in range(len(response['game_indices'])):
    if i < len(response['game_indices'])-1:
        games += (response['game_indices'][i]['version']['name']) + ", "
    else:
        games += (response['game_indices'][i]['version']['name']) + "."



print(" Nome: %s \n Tipo: %s \n Jogos que em aparece: %s " % (response['name'],response['types'][0]['type']['name'], games))


