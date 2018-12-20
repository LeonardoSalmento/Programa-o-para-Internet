import requests

url = "https://reqres.in/"

response = requests.post(url + "api/users" ,data = {"name": "you", "job": "no job"})

print(response)
print(response.json())
