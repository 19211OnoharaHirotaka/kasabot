import requests

url = "https://weather.tsukumijima.net/api/forecast/"
param = {'city':'400040'}

response = requests.get(url,params = param)

print(response.text)