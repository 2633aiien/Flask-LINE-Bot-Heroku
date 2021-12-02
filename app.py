import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

bot_info = line_bot_api.get_bot_info()

print(bot_info.display_name)
print(bot_info.user_id)
print(bot_info.basic_id)
print(bot_info.premium_id)
print(bot_info.picture_url)
print(bot_info.chat_mode)
print(bot_info.mark_as_read_mode)

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if(event.message.text == "醫院資訊"):
        message = TextSendMessage("醫院資訊")
    if(event.message.text == "我要預約"):
        message = TextSendMessage("我要預約")
    if(event.message.text == "資訊"):
        message = TextSendMessage(str(bot_info.user_id))
    if(event.message.text == "我"):
        message = TextSendMessage(bot_info.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        message)
