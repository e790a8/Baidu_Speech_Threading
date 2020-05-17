#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/05/16
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : test.py

import baidu_speech

if __name__ == '__main__':
    App_ID = "" # 17xxxx0x
    API_Key = ""    # xxxxv8lbtxxxxNQG4lhxxxx
    Secret_Key = "" # xxxxDclQ4pUwxxxxQXHGcVISoxxxxxDx
    test = baidu_speech.Baidu_speech(App_ID,API_Key,Secret_Key)
    test.getMp3("test.txt")
    # test.getMp3("test.txt","test.mp3",False,{"spd":5,"pit":5,"vol":5,"per":0})