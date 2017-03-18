# coding=utf-8
import itchat
from itchat.content import *
import requests
import json
import urllib
import time

global fromUserName
fromUserName = None

#私聊
@itchat.msg_register(itchat.content.TEXT, isMpChat=False)
def text_reply(msg):
    global fromUserName
    fromUserName = msg['FromUserName']
    msgToSend = msg['Text']
    print msgToSend
    itchat.send_msg(msgToSend, "xiaoice-ms")

#群聊且@了
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    global fromUserName
    if msg['isAt']:
        fromUserName = msg['FromUserName']
        msgToSend = msg['Text'][5:]
        print msgToSend
        itchat.send_msg(msgToSend, "xiaoice-ms")

#小冰的文本回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    global fromUserName
    itchat.send_msg(msg['Text'], fromUserName)

#小冰的图片、语音、视频等回复
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
def download_files(msg):
    global fromUserName
    msg['Text'](msg['FileName'])
    msgToSend = '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

    if msgToSend[:5] == '@fil@':
        itchat.send_file(msgToSend[5:], fromUserName)
    elif msgToSend[:5] == '@img@':
        itchat.send_image(msgToSend[5:], fromUserName)
    elif msgToSend[:5] == '@vid@':
        itchat.send_video(msgToSend[5:], fromUserName)
    else:
        itchat.send_msg(msgToSend, fromUserName)


itchat.auto_login()
itchat.run()
