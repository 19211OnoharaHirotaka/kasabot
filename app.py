#-*- coding: utf-8 -*-

# インポートするライブラリ
from flask import Flask, request, abort, render_template, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction,
    MessageTemplateAction, URITemplateAction, StickerMessage,
    URIAction, RichMenu, PostbackEvent
)

import os
import json
import numpy

import requests
import pprint
from datetime import datetime
import re


# ウェブアプリケーションフレームワーク:flaskの定義
app = Flask(__name__)

# サーバの環境変数から LINE_Access_Tokenを取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# サーバの環境変数から LINE_Channel_Secretを取得
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
handler = WebhookHandler(LINE_CHANNEL_SECRET)



# "/"にGETリクエストを送ると返す  (ルートのアドレスに以下のものを配置することを明言)
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot"



# LINE側が送ってきたメッセージが正しいか検証する
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # プログラムの通常の操作中に発生したイベントの報告
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名検証で失敗したときは例外をあげる
        abort(400)
    return jsonify({"state": 200})



# MessageEvent　テキストメッセージ受け取った時
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 受け取りデータの確認
    print(f"\nevent：{event}\n")
    print(f"\n{event}\n")

    # 受け取ったメッセージ
    text = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    profile.user_id #-> ユーザーID
    user_id = f"{profile.user_id}"

    if "おはよう" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Good morning")
         )
    elif "こんにちは" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello World")
         )
    elif "たい" in text:
        img_url = "https://taisoda-ezaki-lab.herokuapp.com/static/images/tai.png"
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="たい！"),
                ImageSendMessage(img_url, img_url)
            ]
         )
    elif "ぶり" in text:
        img_url = "https://taisoda-ezaki-lab.herokuapp.com/static/images/tai.png"
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="ぶり!!"),
                ImageSendMessage(img_url, img_url)
            ]
        )

    elif "url" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="https://dotinstall.com/")
        )

    elif "google" in text:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="googleのサイトです"),
                TextSendMessage(text="https://www.google.com/")
            ]
         )

    elif "何したの" in text:            
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="こんにちは"),
                TextSendMessage(text="今日はプログラミングの勉強をしました"),
                TextSendMessage(text="難しかったです")
            ]
        )

    # elif "通知" in text:
    #     # 全ユーザにプッシュ
    #     line_bot_api.broadcast(
    #         TextSendMessage(text="通知テスト")
    #     )   

    # elif "全員通知" in text:
    #     # 全ユーザにプッシュ
    #     img_url = "https://1.bp.blogspot.com/-Q9jOqnVqGuo/W64DqXTxwfI/AAAAAAABPIk/mn0XoaVlL2s_Sphqb-5WielV75A6JIEowCLcBGAs/s800/job_yarigai_sausyu.png"
    #     line_bot_api.broadcast(
    #         [
    #             TextSendMessage(text="全ユーザーに通知します"),
    #             ImageSendMessage(img_url, img_url)
    #         ]
    #     )   

    elif "ユーザーid" in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{profile.user_id}")
         )

    elif "idを送る" in text:
        messages = TextSendMessage(text="Hellow!!")
        line_bot_api.push_message(user_id, messages=messages)

    elif "天気" in text:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="気象庁のサイトです\n\nhttps://www.jma.go.jp/bosai/map.html#6/31.128/137.285/&contents=forecast\nhttps://www.jma.go.jp/bosai/forecast/")
            ]
         )
         
    elif "傘" in text:
        #現在の時刻を取得
        today = datetime.now()
        hour = today.hour


        #天気予報APIのurlとクエリ
        url_tenki = "https://weather.tsukumijima.net/api/forecast/"
        param = {'city':'240010'}
        # APIからのレスポンス
        response = requests.get(url_tenki, params = param)
        #pythonの辞書に変換
        data = response.json()
        place = data['publishingOffice']

        #直近の時間ごとに取得する降水確率を変える
        if hour >= 0 and hour <= 6:
            chanceOfRain = data['forecasts'][0]['chanceOfRain']['T00_06']
            result = re.sub(r"\D", "", chanceOfRain)
            ame = int(result)
            kasa = ''
            if ame >= 20 and ame <= 60:
                kasa = '折り畳み傘を忘れずに持って行ってください。'
            elif ame >= 60:
                kasa = '長傘を忘れずに持って行ってください。'
            else:
                kasa = '傘を持って行かなくて大丈夫です。'

        elif hour >= 6 and hour <= 12:
            chanceOfRain = data['forecasts'][0]['chanceOfRain']['T06_12']
            result = re.sub(r"\D", "", chanceOfRain)
            ame = int(result)
            kasa = ''
            if ame >= 20 and ame <= 60:
                kasa = '折り畳み傘を忘れずに持って行ってください。'
            elif ame >= 60:
                kasa = '長傘を忘れずに持って行ってください。'
            else:
                kasa = '傘を持って行かなくて大丈夫です。'

        elif hour >= 12 and hour <=18:
            chanceOfRain = data['forecasts'][0]['chanceOfRain']['T12_18']
            result = re.sub(r"\D", "", chanceOfRain)
            ame = int(result)
            kasa = ''
            if ame >= 20 and ame <= 60:
                kasa = '折り畳み傘を忘れずに持って行ってください。'
            elif ame >= 60:
                kasa = '長傘を忘れずに持って行ってください。'
            else:
                kasa = '傘を持って行かなくて大丈夫です。'

        else:
            chanceOfRain = data['forecasts'][0]['chanceOfRain']['T18_24']
            result = re.sub(r"\D", "", chanceOfRain)
            ame = int(result)
            kasa = ''
            if ame >= 20 and ame <= 60:
                kasa = '折り畳み傘を忘れずに持って行ってください。'
            elif ame >= 60:
                kasa = '長傘を忘れずに持って行ってください。'
            else:
                kasa = '傘を持って行かなくて大丈夫です。'
        # chanceOfRain_today = data['forecasts'][0]['chanceOfRain']['T00_06']
        # chanceOfRain_tomorrow = data['forecasts'][1]['chanceOfRain']['T00_06']
        # chanceOfRain_tomorrow2 = data['forecasts'][2]['chanceOfRain']['T00_06']


        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=f"降水確率は{chanceOfRain}です。\n{kasa}")
            ]
         )

    else:
    	line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「" + text + "」って何？")
         )




if __name__ == "__main__":
    port = int(os.getenv("PORT",8080))
    app.run(host="0.0.0.0", port=port)
#こんにちは2022.02.20.01:04a.m.