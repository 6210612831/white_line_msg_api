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
        def create_user(user_id):
            account_serializer = AccountSerializer(data={'user_id':str(user_id)})
            if account_serializer.is_valid(raise_exception=True):
                account_serializer.save()       

        def join_group(message,user_id):
            name = message[message.find("join group ")+len("join group "):]
            account = Account.objects.filter(user_id=user_id)
            group = Audience.objects.filter(name = name)
            # Create account if not exist
            if len(account) == 0 :
                create_user(user_id)
                account = Account.objects.filter(user_id=user_id)
                print("ACCOUNT : ",account)

            # Append group
            if len(group) != 0:
                account[0].group.append(group)
                account[0].group.save()
                return "Join group name :"+ name
            else:
                return "No group name :"+ name
        
        def create_group(message,user_id):
            name = message[message.find("create group ")+len("create group "):]
            account = Account.objects.filter(user_id=user_id)
            group = Audience.objects.filter(name = name)
            print(account)
            print(len(account))
            print(account[0].is_admin)
            # Check user permission to create group
            if len(account) == 0 or (not account[0].is_admin):
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
                create_user(user_id)
                account = Account.objects.filter(user_id=user_id)
                print("ACCOUNT : ",account)
                return "You didn't join group name :"+name

            # Append group
            if len(group) != 0:
                try:
                    account[0].group.remove(group)
                    account[0].group.save()
                except:
                    return "You didn't join group name :"+name
                return "Leave group name :"+name
            else:
                return "No group name :"+ name
        
        def group_list(user_id):
            account = Account.objects.filter(user_id=user_id)
            # Create account if not exist
            if len(account) == 0 :
                create_user(user_id)
                account = Account.objects.filter(user_id=user_id)
                print("ACCOUNT : ",account)
                return "You didn't join any group"

            text = "Your group name : "    
            for group_name in account[0].group.all():
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

        def set_admin(user_id):
            account = Account.objects.filter(user_id=user_id)
            print("ACCOUNT SUPER ADMIN : ",account)
            account[0].is_admin = True
            account[0].save()
            return "Set admin done!"

        def clear():
            accounts = Account.objects.all()
            for account in accounts:
                account.delete()
            print(Account.objects.all())
            return "delete done!"

        def check_message(message,user_id):
            message = message.lower()
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
            elif message.find("setadmin")!= -1:
                return set_admin(user_id)
            elif message.find("clearaccount")!= -1:
                return clear()
            return message


        global CHANNEL_SECRET,CHANNEL_ACCESS_TOKEN

        token = json.loads(request.body.decode("utf-8") )
        message = token["events"][0]["message"]["text"]
        userId = token["events"][0]["source"]["userId"]

        print(f"request.body : {request.body}")
        print(f"request.headers : {request.headers}")

        return_to_user_text = check_message(message,userId)

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



def index(request):
    return render(request,"message_api/index.html")



