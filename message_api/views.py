from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
import requests
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
AUDIENCEGROUPID = 8692370298889


# Create your views here.
class MessageApiView(APIView):

    def get(self, request, *args, **kwargs):
         return Response("serializer.data", status=status.HTTP_200_OK)

   # def isUserIdExistInAudienceGroup():
        

    def post(self, request, *args, **kwargs):
        
        global CHANNEL_SECRET,CHANNEL_ACCESS_TOKEN
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        # parser = WebhookParser(CHANNEL_SECRET)

        token = json.loads(request.body.decode("utf-8") )

        userId = token["events"][0]["source"]["userId"]
        message = str(token["events"][0]["message"]["text"])
        replay_token = token["events"][0]["replyToken"]
        # CheckUserId = False

        print(f"request.body : {request.body}")
        print(f"request.headers : {request.headers}")
        # print("replyToken",token["events"][0]["replyToken"])
        # print("text",token["events"][0]["message"]["text"])
        print(message)

        headers = {"Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"}

        # Check user id is valid
        # if  requests.get(f"https://api.line.me/v2/bot/profile/{userId}", headers=headers).status_code == 200:
        #     CheckUserId = True

        # If message = "add_me_to_audience_group" and userId is valid
        if message == "add_me_to_audience_group":
            # PUT UserId to audienceGroup
            url = f'https://api.line.me/v2/bot/audienceGroup/upload'
            headers = {'content-type': 'application/json',
                     "Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"
            }
            payload = {
                    "audienceGroupId": f"{AUDIENCEGROUPID}",
                    "uploadDescription": "Add useId",
                    "audiences": 
                        [
                            {
                                "id": f"{userId}"
                            }
                        ]
            }
            res = requests.put(url, headers=headers,data=json.dumps(payload))
            if res.status_code != 200:
                print("Can't add UserId to audienceGroup")
            else:
                line_bot_api.reply_message(
                replay_token ,
                TextSendMessage("Add you to user pool is done!!")
            )
            
        if len(replay_token) != 0:
            line_bot_api.reply_message(
                replay_token ,
                TextSendMessage("Reply : "+message)
            )
        else:
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("", status=status.HTTP_200_OK)


def index(request):
    return render(request,"message_api/index.html")



