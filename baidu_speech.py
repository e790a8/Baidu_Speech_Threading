#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/05/16
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : baidu_speech.py

from aip import AipSpeech
from pathlib import Path
from tqdm import tqdm

class Baidu_speech:
    __isConnect = False
    __Text_data = []
    __File_save_path = None
    __Mp3_Option = dict()
    __Mp3 = []
    __Mp3_Error = []
    __Error = "Connection Error Please Again Input!!!"
    def __init__(self,app_id:str,api_key:str,secret_key:str):
        self.__App_ID = app_id
        self.__API_Key = api_key
        self.__Secret_Key = secret_key
        self.__baidu_conn()

    def __baidu_conn(self):
        self.__Baidu_connection = AipSpeech(self.__App_ID,self.__API_Key,self.__Secret_Key)
        if self.__check_baidu_conn() == False:
            raise self.__Error
            self.__isConnect = False
        else:
            print("Connection Success!!!")
            self.__isConnect = True

    def __check_baidu_conn(self):
        try:
            check = self.__Baidu_connection.synthesis("测试",'zh',1,{'vol':5})
            return True
        except:
            return False

    def __check_file_type(self,File_path:Path):
        if File_path.suffix == ".txt":
            self.__File_path = File_path
            self.__File_save_path = str(File_path)[:str(File_path).find(".")]+ ".mp3"
            self.__txt_data()
            return True
        else:
            raise "Only support：txt"
            return False

    def __check_file_path(self,File_path:str):
        Path_File_path = Path(File_path)
        if Path_File_path.is_file() and self.__check_file_type(Path_File_path):
            return True
        else:
            raise "File Not Find!!!"
            return False

    def __check_file_save_path(self,File_save_path:str):
        if Path(File_save_path).exists():
            if Path(File_save_path).is_dir():
                self.__File_save_path = File_save_path+"/"+self.__File_save_path
            else:
                self.__File_save_path = File_save_path
        else:
            if -1 in [File_save_path.find("/"),File_save_path.find("\\")]:
                if File_save_path.find(".mp3") != -1:
                    self.__File_save_path = File_save_path
                else:
                    self.__File_save_path = File_save_path+".mp3"
            elif File_save_path.find(".mp3") != -1:
                self.__File_save_path = File_save_path
            else:
                raise "Directory Not Find!!!"
                return False


    def __check_option(self,Option):
        try:
            sdp_pit = lambda x: x >= 0 and x <= 9
            vol = lambda x: x >= 0 and x <= 15
            per = lambda x: x >= 0 and x <= 5
            try:
                if sdp_pit(Option['spd']):
                    self.__Mp3_Option['spd'] = Option['spd']
                elif Option['spd'] < 0:
                    print("spd < 0 default spd = 0")
                    self.__Mp3_Option['spd'] = 0
                elif Option['spd'] > 9:
                    print("spd > 9 default spd = 9")
                    self.__Mp3_Option['spd'] = 9
            except:
                self.__Mp3_Option['spd'] = 5
            try:
                if sdp_pit(Option['pit']):
                    self.__Mp3_Option['pit'] = Option['pit']
                elif Option['pit'] < 0:
                    print("pit < 0 default pit = 0")
                    self.__Mp3_Option['pit'] = 0
                elif Option['pit'] > 9:
                    print("pit > 9 default pit = 9")
                    self.__Mp3_Option['pit'] = 9
            except:
                self.__Mp3_Option['pit'] = 5
            try:
                if vol(Option['vol']):
                    self.__Mp3_Option['vol'] = Option['vol']
                elif Option['vol'] < 0:
                    print("vol < 0 default vol = 0")
                    self.__Mp3_Option['vol'] = 0
                elif Option['vol'] > 15:
                    print("vol > 15 default vol = 15")
                    self.__Mp3_Option['vol'] = 15
            except:
                self.__Mp3_Option['vol'] = 5
            try:
                if per(Option['per']):
                    self.__Mp3_Option['per'] = Option['per']
                elif Option['per'] < 0:
                    print("per < 0 default per = 0")
                    self.__Mp3_Option['per'] = 0
                elif Option['per'] > 5:
                    print("per > 5 default per = 5")
                    self.__Mp3_Option['per'] = 5
            except:
                self.__Mp3_Option['per'] = 0
        except:
            raise "Option Error True:{'spd':0-9,'pit':0-9,'vol':0-15,'per':0-5} This Option is Negligible!!!"

    def __txt_data(self):
        try:
            with open(self.__File_path,"rb") as f:
                data = f.readlines()
                f.close()
            for i in data:
                temp = i.decode("utf-8")
                if len(temp) > 1024:
                    index = 0
                    for q in range(1,(len(temp) // 1024) + 1):
                        self.__Text_data.append(temp[index:index + (1023 * q)])
                        index += 1023 * q
                else:
                    self.__Text_data.append(i)
        except:
            raise "Text data encode not is utf-8"

    def __post_data(self,is_Open_Threading:bool):
        if is_Open_Threading:
            raise "Temporarily Unsupported Threading.I'm Sorry"
            return False
        else:
            for i in tqdm(self.__Text_data):
                temp = self.__Baidu_connection.synthesis(i,'zh',1,self.__Mp3_Option)
                self.__Mp3.append(temp) if not isinstance(temp,dict) else self.__Mp3_Error.append(i)
            if self.__Mp3_Error != []:
                print("Have "+str(len(self.__Mp3_Error))+" Error\nuse：.getErrorList")
    def __save_data(self):
        try:
            with open(self.__File_save_path,"wb") as f:
                for i in self.__Mp3:
                    f.write(i)
                f.close()
                print("File Save Success!!!")
        except:
            raise "File Save Error!!!"

    def getErrorList(self):
        return self.__Mp3_Error

    def getMp3(self,File_path:str,File_save_path = None,is_Open_Threading = False,Option = None):
        if self.__isConnect:
            if self.__check_file_path(File_path):
                if isinstance(Option,dict):
                    self.__check_option(Option)
                if File_save_path != None:
                    self.__check_file_save_path(File_save_path)
                self.__post_data(is_Open_Threading)
                self.__save_data()
        else:
            raise self.__Error
            return False