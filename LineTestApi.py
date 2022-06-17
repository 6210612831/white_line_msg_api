import json
import requests


token = "JtUxiyw8orHxQEgjPiFWXrQsYEYxnnNiSrnAwhzoXAJznUZLr/WqO7iWb76m/dqR2WBdox+hjeCwUVn8ApuVrVz833kAzrtFETGXx8fou0XnGrcwM++A0S/AZX0ygUii02fHLZpnw5V0zd3zK67MQwdB04t89/1O/w1cDnyilFU="
audienceGroupId=8692370298889
userId = "Ud3893b9950b8db28b49b95bfbaa408e0"




# -------------------- CREATE audienceGroup -------------------- 

# url = 'https://api.line.me/v2/bot/audienceGroup/upload'
# payload = {"description": "test_name_1"}
# headers = {'content-type': 'application/json',
#          "Authorization" : f"Bearer {token}"
# }
# res = requests.post(url, data=json.dumps(payload), headers=headers)


# -------------------- DELETE audienceGroup -------------------- 

# url = f'https://api.line.me/v2/bot/audienceGroup/{audienceGroupId}'
# headers = {"Authorization" : f"Bearer {token}"}
# res = requests.delete(url, headers=headers)


# --------------------  GET data of audienceGroup -------------------- 

# url = f'https://api.line.me/v2/bot/audienceGroup/{audienceGroupId}'
# headers = {"Authorization" : f"Bearer {token}"}
# res = requests.get(url, headers=headers)


# -------------------- PUT UserId to audienceGroup -------------------- 

# url = f'https://api.line.me/v2/bot/audienceGroup/upload'
# headers = {'content-type': 'application/json',
#          "Authorization" : f"Bearer {token}"
# }
# payload = {
#         "audienceGroupId": f"{audienceGroupId}",
#         "uploadDescription": "Add useId",
#         "audiences": 
#             [
#                 {
#                     "id": f"{userId}"
#                 }
#             ]
# }
# res = requests.put(url, headers=headers,data=json.dumps(payload))


# -------------------- POST Message to user -------------------- 

# url = f'https://api.line.me/v2/bot/message/multicast'
# headers = {'content-type': 'application/json',
#          "Authorization" : f"Bearer {token}"
# }
# payload = {
#         "to": [f"{userId}"],
#         "messages": 
#             [
#                 {
#                     "type":"text",
#                     "text":"Hello, world"
#                 }
#             ]
# }
# res = requests.post(url, headers=headers,data=json.dumps(payload))


# --------------------  GET All Audience data -------------------- 

# url = f'https://api.line.me/v2/bot/audienceGroup/list'
# headers = {'content-type': 'application/json',
#          "Authorization" : f"Bearer {token}"
# }
# payload = {
#         "to": [f"{userId}"],
#         "messages": 
#             [
#                 {
#                     "type":"text",
#                     "text":"Hello, world"
#                 }
#             ]
# }
# res = requests.get(url, headers=headers)



# --------------------  Push Message To User Pool(AudienceGroup) -------------------- 

# url = f'https://api.line.me/v2/bot/message/narrowcast'
# headers = {'content-type': 'application/json',
#          "Authorization" : f"Bearer {token}"
# }
# payload = {
#             "messages": 
#             [
#                 {
#                     "type":"text",
#                     "text":"Hello World To Audience Group"
#                 }
#             ],
#             "recipient": 
#             {
#                     "type": "audience",
#                     "audienceGroupId": audienceGroupId
#             }     
# }
# res = requests.post(url, headers=headers,data=json.dumps(payload))



print(res.status_code)
print(res.headers)
print(res.json())
