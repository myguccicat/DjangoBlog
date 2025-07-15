from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            print("收到訊息", event, "\n")
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    print("收到訊息:", event.message.text, "\n")

                    if event.message.text == "###報到領域:藝術":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="歡迎來到藝術領域！請問你想了解什麼？")
                        )
                    elif event.message.text == "###你是user":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="是的，我是user！")
                        )
                    elif event.message.text == "###你的車牌號碼就是你想說的":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=f"你的車牌號碼是: {event.message.text}")
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="抱歉，現在不方便喔。")
                        )
                else:
                    print("文字以外的類型\n")
            else:
                print("非訊息事件\n")

    return HttpResponse()
