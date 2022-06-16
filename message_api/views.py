from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
import os
import sys
import wsgiref.simple_server
from argparse import ArgumentParser

from builtins import bytes
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.utils import PY3
from django.shortcuts import render
import json

CHANNEL_SECRET = "2fd29402f72edea813df01ad10854262"
CHANNEL_ACCESS_TOKEN = "JtUxiyw8orHxQEgjPiFWXrQsYEYxnnNiSrnAwhzoXAJznUZLr/WqO7iWb76m/dqR2WBdox+hjeCwUVn8ApuVrVz833kAzrtFETGXx8fou0XnGrcwM++A0S/AZX0ygUii02fHLZpnw5V0zd3zK67MQwdB04t89/1O/w1cDnyilFU="




# Create your views here.
class MessageApiView(APIView):

    def get(self, request, *args, **kwargs):
         return Response("serializer.data", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        global CHANNEL_SECRET,CHANNEL_ACCESS_TOKEN
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        # parser = WebhookParser(CHANNEL_SECRET)

        token = json.loads(request.body.decode("utf-8") )

        # print(f"request.body : {request.body}")
        # print(f"request.headers : {request.headers}")
        # print("replyToken",token["events"][0]["replyToken"])
        # print("text",token["events"][0]["message"]["text"])
        try:
            line_bot_api.reply_message(
                token["events"][0]["replyToken"],
                TextSendMessage(token["events"][0]["message"]["text"])
            )
        except:
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("", status=status.HTTP_200_OK)


def index(request):
    return render(request,"message_api/index.html")



