#!/usr/bin/env python3
# coding: utf-8

from wxpy import *

import requests
from json import JSONDecoder

import hashlib
import cv2
import time
import random
import os,sys
import string
import base64
import requests
import numpy as np
from urllib.parse import urlencode
import json
import threading

from PIL import Image
from pyzbar import pyzbar



from aip import AipImageCensor
from aip import AipNlp
APP_ID = '11685556'
API_KEY = 'ELS0CGtNxbq15Gs0GGyP8xx8'
SECRET_KEY = 'U5U5LHnsaDcErfguBOBTlGjR107i5hku'
client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)




""" 你的 APPID AK SK """
APP_ID2 = '14895115'
API_KEY2 = 'oxGumTKpYGZfxokP7iPayTKB'
SECRET_KEY2 = 'UYlln10MWlrW3EVUH0wDYDn2TIKc9BmM'
client2 = AipNlp(APP_ID2, API_KEY2, SECRET_KEY2)


def remote_reup():
    bot.registered.enable()

def remote_down():
    bot.registered.disable()
    bot.registered.enable(remote_up)

def remote_reup():
    bot.registered.enable()



def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()



import cv2


bot = Bot(cache_path=True)

myself = bot.self

group_1 = bot.groups().search('aiaiai')[0]

group_2 = bot.groups().search('幼儿园接送巴士🚍')[0]

group_3 = bot.groups().search('13物联网班微信群')[0]

group_4 = bot.groups().search('韶大花都群')[0]

group_free = [group_1,group_2,group_4]


@bot.register([Group],except_self=False)
def remote_up(msg):
    if (msg.member == myself and 'bot start' in msg.text):
        thread = threading.Thread(target=remote_reup)
        thread.start()
        thread.join()
        msg.reply('--言论舆情检测已启动--')
        msg.reply('请谨慎发言！')


@bot.register([Friend],TEXT)
def reply_my_friend(msg):
    url = "https://aip.baidubce.com/rest/2.0/antispam/v2/spam"

    querystring = {"access_token":"24.f497c07f1abcb5d5c4f6f32052878972.2592000.1545452794.282335-11685556"}

    payload = {"content": msg.text}
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Postman-Token': "a7b8ce55-437b-49b3-8a38-fc6e5b7cc020"
    }

    responsess = requests.post(url, data=payload, headers=headers, params=querystring).json()


    if responsess['result']['spam']!=0:
        resbi=responsess['result']['review']+responsess['result']['reject']
        resshenhe='---------\n\n您的本次发言：\n【'+msg.text+'】\n存在违规情况：\n\n'
        for rb in resbi:
            if rb['label']==1:
                rblabel='暴恐违禁'
            elif rb['label']==2:
                rblabel='文本色情'
            elif rb['label']==3:
                rblabel='政治敏感'
            elif rb['label']==4:
                rblabel='恶意推广'
            elif rb['label']==5:
                rblabel='低俗辱骂'

            resshenhe = resshenhe + rblabel + '：' + '{:.2f}%\n'.format(rb['score']*100)
        msg.reply(resshenhe + '\n---------\n本次违规发言记录已提交给网警，请在24小时内去最近的派出所投案自首')





@bot.register(group_free,TEXT,except_self=False)
def auto_reply(msg):

    if (msg.member == myself and 'bot shutdown' in msg.text):
        thread = threading.Thread(target=remote_down)
        thread.start()
        thread.join()
        msg.reply('--言论舆情检测已关闭--')
    elif (msg.member == myself and '启动' in msg.text):
        thread = threading.Thread(target=remote_up)
        thread.start()
        thread.join()
        msg.reply('--言论舆情检测已启动--')


    url = "https://aip.baidubce.com/rest/2.0/antispam/v2/spam"
    querystring = {"access_token":"24.f497c07f1abcb5d5c4f6f32052878972.2592000.1545452794.282335-11685556"}
    payload = {"content": msg.text}
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Postman-Token': "a7b8ce55-437b-49b3-8a38-fc6e5b7cc020"
    }




    responsess = requests.post(url, data=payload, headers=headers, params=querystring).json()


    if responsess['result']['spam']!=0:

        resbi=responsess['result']['review']+responsess['result']['reject']
        resshenhe='---------\n\n检测到'+str(msg.member)+'的发言：\n【'+msg.text+'】\n存在违规情况：\n\n'
        for rb in resbi:
            if rb['label']==1:
                rblabel='暴恐违禁'
            elif rb['label']==2:
                rblabel='文本色情'
            elif rb['label']==3:
                rblabel='政治敏感'
            elif rb['label']==4:
                rblabel='恶意推广'
            elif rb['label']==5:
                rblabel='低俗辱骂'

            resshenhe = resshenhe + rblabel + '：' + '{:.2f}%\n'.format(rb['score']*100)
        msg.reply(resshenhe + '\n---------\n本次违规发言记录已提交给网警，请在24小时内去最近的派出所投案自首')





@bot.register([Friend],PICTURE)
def ai_reply(msg):

    image_name = msg.file_name

    msg.get_file('' + msg.file_name)

    f=open(image_name,'rb')

    img = base64.b64encode(f.read())   #得到API可以识别的字符串


    image = get_file_content(image_name)
    resccc=client.imageCensorUserDefined(image);

    rescul='--------------------\n\n检测到你的图片存在违规情况：\n\n'
    if resccc['conclusionType']!=1:
        for ms in resccc['data']:
            if ms['type']==8 or ms['type']==11:
                rescul=rescul+ms['msg']+'：'+ms['stars'][0]['name']+'\n'
            else:
                rescul=rescul+ms['msg']+'({:.0f}%)\n'.format(ms['probability']*100)
        rescul=rescul+'\n--------------------\n'+'本次违规图片已提交给网警，请在24小时内去最近的派出所投案自首'
        msg.reply(rescul)







@bot.register(group_free,PICTURE)
def ai_replygg(msg):

    image_name = msg.file_name

    msg.get_file('' + msg.file_name)

    f=open(image_name,'rb')

    img = base64.b64encode(f.read())   #得到API可以识别的字符串


    image = get_file_content(image_name)
    resccc=client.imageCensorUserDefined(image);








    if resccc['conclusionType']!=1:
        for ms in resccc['data']:
            if ms['type']==6:
                rescuqr='--------------------\n\n检测到\n'+str(msg.member)+'\n的图片含二维码\n\n--------------------\n\n'

                res=pyzbar.decode(Image.open(image_name), symbols=[pyzbar.ZBarSymbol.QRCODE])

                rescuqr=rescuqr+'已将二维码解析成原始数据:\n\n'+str(res[0].data,"utf-8")

                msg.reply(rescuqr)
                flag=1



    if resccc['conclusionType']!=1:
        if len(resccc['data'])==1 and flag==1:
            flag=0
        else:
            rescul='--------------------\n\n检测到'+str(msg.member)+'的图片存在违规情况：\n\n'
            rescull='\n--------------------\n'+'本次违规图片已提交给网警，请在24小时内去最近的派出所投案自首'
            for ms in resccc['data']:
                if ms['type']==8 or ms['type']==11:
                    rescul=rescul+ms['msg']+'：'+ms['stars'][0]['name']+'\n'
                elif ms['type']!=6:
                    rescul=rescul+ms['msg']+'({:.0f}%)\n'.format(ms['probability']*100)
            rescul=rescul+rescull
            msg.reply(rescul)















embed()