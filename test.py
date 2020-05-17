#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/05/18
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : test.py

import baidu_speech

if __name__ == '__main__':
    App_ID = "17183601"
    API_Key = "zWW6v8lbtOpGRNQG4lhtnakP"
    Secret_Key = "kfOyDclQ4pUw3y0UQXHGcVISofpIDxDz"
    test = baidu_speech.Baidu_speech(App_ID,API_Key,Secret_Key)
    test.getMp3("test.txt")
    # test.getMp3("test.txt",is_Open_Threading=True)
    # test.getMp3("test.txt","./test.mp3",False,{"spd":5,"pit":5,"vol":5,"per":0})