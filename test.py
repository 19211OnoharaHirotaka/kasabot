import requests
import pprint

#天気予報APIのurlとクエリ
url = "https://weather.tsukumijima.net/api/forecast/"
param = {'city':'240010'}

# APIからのレスポンス
response = requests.get(url, params = param)
#pythonの辞書に変換
data = response.json()
# pprint.pprint(data['forecasts'][2])

# a = type(int(data['forecasts'][0]['chanceOfRain']['T00_06']))

pprint.pprint (data['publishingOffice'])
pprint.pprint (data['forecasts'][0]['chanceOfRain']['T00_06']) #今日
pprint.pprint (data['forecasts'][1]['chanceOfRain']['T00_06']) #明日
pprint.pprint (data['forecasts'][2]['chanceOfRain']['T00_06']) #明後日
# pprint.pprint (a)

# print(type(data))