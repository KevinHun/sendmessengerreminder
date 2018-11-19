import fbchat
import json
from getpass import getpass
from fbchat.models import *

username = 'kevin.hunyadi@gmail.com'
client = fbchat.Client(username, getpass())

# load the json data
with open('messages.json') as json_data:
    jsonfile = json.load(json_data)


for msg in jsonfile["messages"]:
    print(msg)
    userList = client.searchForUsers(msg['receiver'])
    receiver = userList[0]
    client.send(Message(text=msg['text']), thread_id=receiver.uid, thread_type=ThreadType.USER)

client.logout()