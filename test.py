import requests
import pprint
import re

#天気予報APIのurlとクエリ
url = "https://weather.tsukumijima.net/api/forecast/"
param = {'city':'150020'}

# APIからのレスポンス
response = requests.get(url, params = param)
#pythonの辞書に変換
data = response.json()
# pprint.pprint(data['forecasts'][2])

# a = type(int(data['forecasts'][0]['chanceOfRain']['T00_06']))

#文字列から数字のみを取り出す処理
a = data['forecasts'][1]['chanceOfRain']['T00_06']
result = re.sub(r"\D", "", a)

pprint.pprint (data['publishingOffice'])
# pprint.pprint (data['forecasts'][0]['chanceOfRain']['T00_06']) #今日
# pprint.pprint (data['forecasts'][1]['chanceOfRain']['T00_06']) #明日
# pprint.pprint (data['forecasts'][2]['chanceOfRain']['T00_06']) #明後日

pprint.pprint (data['forecasts'][0]['chanceOfRain']) #今日
pprint.pprint (data['forecasts'][1]['chanceOfRain']) #明日
pprint.pprint (data['forecasts'][2]['chanceOfRain']) #明後日
print (result)



# pprint.pprint (a)

# print(type(data))