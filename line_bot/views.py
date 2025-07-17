from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import LocationMessage, LocationSendMessage
from linebot.models import StickerMessage, StickerSendMessage
from linebot.models import ImageMessage, ImageSendMessage


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
                    elif event.message.text == "Test":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="{}media/{}".format(request.build_absolute_uri('/'), "myguccicat.jpg"))
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="抱歉，現在不方便。")
                        )
                elif isinstance(event.message, LocationMessage):
                    print("收到位置訊息:", event, "\n")
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="緯度:{}, 經度:{}".format(event.message.latitude, event.message.longitude))
                        )
                elif isinstance(event.message, StickerMessage):
                    print("收到貼圖訊息:", event.message, "\n")
                    line_bot_api.reply_message(
                        event.reply_token,
                        StickerSendMessage(
                            package_id=11539,
                            sticker_id=52114110
                        )
                
                    )
                elif isinstance(event.message, ImageMessage):
                    print("收到圖片", event.message)
                    image_name = event.message.id + ".jpg"
                    image_content = line_bot_api.get_message_content(event.message.id)
                    path = "./public/uploads/" + image_name
                    with open(path, 'wb') as fd:
                        for chunk in image_content.iter_content():
                            fd.write(chunk)

                    reply_image_path = "http://{}/media/{}".format(request.get_host(), image_name)
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageMessage(
                            preview_image_url=reply_image_path,
                            original_content_url=reply_image_path,
                        )
                    )
                else:
                    print("文字以外的類型\n")
           
            else:
                print("非訊息事件\n")

    return HttpResponse()
