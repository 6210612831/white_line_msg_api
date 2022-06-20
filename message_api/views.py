from email.headerregistry import Group
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
from message_api.models import Account, Audience

from message_api.serializers import AccountSerializer,AudienceSerializer

CHANNEL_SECRET = "2fd29402f72edea813df01ad10854262"
CHANNEL_ACCESS_TOKEN = "JtUxiyw8orHxQEgjPiFWXrQsYEYxnnNiSrnAwhzoXAJznUZLr/WqO7iWb76m/dqR2WBdox+hjeCwUVn8ApuVrVz833kAzrtFETGXx8fou0XnGrcwM++A0S/AZX0ygUii02fHLZpnw5V0zd3zK67MQwdB04t89/1O/w1cDnyilFU="
AUDIENCEGROUPID = 4735937759476


# Create your views here.
class MessageApiView(APIView):


    

    def get(self, request, *args, **kwargs):
         return Response("serializer.data", status=status.HTTP_200_OK)
  
    def post(self, request, *args, **kwargs):
        def get_audience_count():
            url = f'https://api.line.me/v2/bot/audienceGroup/{AUDIENCEGROUPID}'
            headers = {"Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"}
            res = requests.get(url, headers=headers)
            return res.json()['audienceGroup']['audienceCount']

        def join_group(message,user_id):
            name = message[message.find("join group ")+len("join group "):]
            account = Account.objects.filter(user_id=user_id)
            group = Audience.objects.filter(name = name)
            # Create account if not exist
            if len(account) == 0 :
                account_serializer = AccountSerializer(data={'user_id':user_id})
                if account_serializer.is_valid(raise_exception=True):
                    account_serializer.save()
                account = Account.objects.filter(user_id=user_id)

            # Append group
            if len(group) != 0:
                account.group.append(group)
                account.group.save()
                return "Join group name :"+ name
            else:
                return "No group name :"+ name
        
        def create_group(message,user_id):
            name = message[message.find("create group ")+len("create group "):]
            account = Account.objects.filter(user_id=user_id)
            group = Audience.objects.filter(name = name)

            # Check user permission to create group
            if len(account) == 0 or not account.is_admin:
                return "You not have permission to create group"

            # check if group name is alreay exist
            if len(group) != 0:
                return "Group name "+name+" already exist"
            
            # Create group
            audience_serializer = AudienceSerializer(data={'name':name})
            if audience_serializer.is_valid(raise_exception=True):
                audience_serializer.save()
                return "Group name "+name+" created"
            return "Invalid group name type"
    

        def leave_group(message,user_id):
            name = message[message.find("leave group ")+len("leave group "):]
            account = Account.objects.filter(user_id=user_id)
            group = Audience.objects.filter(name = name)

            # Create account if not exist
            if len(account) == 0 :
                account_serializer = AccountSerializer(data={'user_id':user_id})
                if account_serializer.is_valid(raise_exception=True):
                    account_serializer.save()
                account = Account.objects.filter(user_id=user_id)
                return "You didn't join group name :"+name

            # Append group
            if len(group) != 0:
                try:
                    account.group.remove(group)
                    account.group.save()
                except:
                    return "You didn't join group name :"+name
                return "Leave group name :"+name
            else:
                return "No group name :"+ name
        
        def group_list(user_id):
            account = Account.objects.filter(user_id=user_id)
            # Create account if not exist
            if len(account) == 0 :
                account_serializer = AccountSerializer(data={'user_id':user_id})
                if account_serializer.is_valid(raise_exception=True):
                    account_serializer.save()
                account = Account.objects.filter(user_id=user_id)
                return "You didn't join any group"
            text = "Your group name : "    
            for group_name in account.group:
                text += group_name +","
            return text[:-1]

        def group_all():
            group_all = Audience.objects.all()
            if len(group_all) == 0 :
                return "No any group was created"
            text = "Group name : "    
            for group in group_all:
                text += group.name +","
            return text[:-1]

        def check_message(message,user_id):
            if message.find("join group") != -1:
                return join_group(message,user_id)
            elif message.find("create group") != -1:
                return create_group(message,user_id)
            elif  message.find("leave group") != -1:
                return leave_group(message,user_id)
            elif  message.find("group list") != -1:
                return group_list(user_id)
            elif  message.find("group all") != -1:
                return group_all()
            return message



        global CHANNEL_SECRET,CHANNEL_ACCESS_TOKEN
        # line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        # parser = WebhookParser(CHANNEL_SECRET)

        token = json.loads(request.body.decode("utf-8") )
        message = token["events"][0]["message"]["text"]
        userId = token["events"][0]["source"]["userId"]
        #replay_token = token["events"][0]["replyToken"]

        print(f"request.body : {request.body}")
        print(f"request.headers : {request.headers}")
        # print("replyToken",token["events"][0]["replyToken"])
        # print("text",token["events"][0]["message"]["text"])

        return_to_user_text = check_message(message)

        url = f'https://api.line.me/v2/bot/message/multicast'
        headers = {'content-type': 'application/json',
                    "Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"
            }
        payload = {
                        "to": [f"{userId}"],
                        "messages": 
                            [
                                {
                                    "type":"text",
                                    "text": return_to_user_text
                                }
                            ]
                }

        res = requests.post(url, headers=headers,data=json.dumps(payload))
        print("STATUS FOR PUT MESSAGE TO USER : ",res.status_code,res.json())
        print("MESSAGE TO USER : "+return_to_user_text)
        return Response("", status=status.HTTP_200_OK)


        # If message = "add_me_to_audience_group" and userId is valid
        # if message == "add_me_to_audience_group":

        #     old_audience_count = get_audience_count()

        #     # PUT UserId to audienceGroup
        #     url = f'https://api.line.me/v2/bot/audienceGroup/upload'
        #     headers = {'content-type': 'application/json',
        #              "Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"
        #     }
        #     payload = {
        #             "audienceGroupId": f"{AUDIENCEGROUPID}",
        #             "uploadDescription": "Add useId",
        #             "audiences": 
        #                 [
        #                     {
        #                         "id": f"{userId}"
        #                     }
        #                 ]
        #     }
        #     res = requests.put(url, headers=headers,data=json.dumps(payload))
        #     print("STATUS FOR ADD USER TO AUDIENCEGROUP : ",res.status_code,res.json())

        #     new_audience_count = get_audience_count()

        #     print(f"audience_count old - new : {old_audience_count} - {new_audience_count}")

            # payload = {
            #             "to": [f"{userId}"],
            #             "messages": 
            #                 [
            #                     {
            #                         "type":"text",
            #                         "text":"You have call add me to audience group function"
            #                     }
            #                 ]
            #     }
        #     if new_audience_count == old_audience_count:
        #         #print("Can't add UserId to audienceGroup")
        #         payload["messages"][0]["text"] = "Cant add you to user pool or you alreay exist in user pool"
        #     else:
        #         payload["messages"][0]["text"] = "Add you to user pool complete"
            # url = f'https://api.line.me/v2/bot/message/multicast'
            # headers = {'content-type': 'application/json',
            #         "Authorization" : f"Bearer {CHANNEL_ACCESS_TOKEN}"
            # }
        #     res = requests.post(url, headers=headers,data=json.dumps(payload))
        #     print("STATUS FOR PUT MESSAGE TO USER : ",res.status_code,res.json())
        #     return Response("", status=status.HTTP_200_OK)

            
        # if len(replay_token) != 0:
        #     line_bot_api.reply_message(
        #         replay_token ,
        #         TextSendMessage("Reply : "+ message)
        #     )
        # else:
        #     return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # return Response("", status=status.HTTP_200_OK)

        

    

def index(request):
    return render(request,"message_api/index.html")



