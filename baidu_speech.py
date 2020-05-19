#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/05/19
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : baidu_speech.py

from aip import AipSpeech
from pathlib import Path
from threading import Thread

class Baidu_speech:
    # 是否连接成功
    __isConnect_bool : bool = False
    # 存储文本数据
    __Text_data_dict : dict = dict()
    # 音频文件保存路径
    __File_save_path_str : str = str()
    # 音频文件配置信息
    __Mp3_Option_dict : dict = dict()
    # 成功的音频片段
    __Mp3_list : list= list()
    # 失败的音频片段
    __Mp3_Error_list : list = list()
    # 生成进度
    __Progress_bar_int : int = 0
    # 连接失败提示文本
    __Connect_error_str : str = "Connection Error Please Again Input!!!"

    # 初始化
    def __init__(self,app_id:str,api_key:str,secret_key:str):
        self.__App_ID : str = app_id
        self.__API_Key : str = api_key
        self.__Secret_Key : str = secret_key
        self.__baidu_conn()

    # 连接
    def __baidu_conn(self) -> bool:
        self.__Baidu_connection : object = AipSpeech(self.__App_ID,self.__API_Key,self.__Secret_Key)
        if self.__check_baidu_conn() == False:
            raise self.__Connect_error_str
            self.__isConnect_bool : bool = False
            return False
        else:
            print("Connection Success!!!")
            self.__isConnect_bool : bool = True
            return True

    # 检查连接
    def __check_baidu_conn(self) -> bool:
        try:
            check = self.__Baidu_connection.synthesis("测试",'zh',1,{'vol':5})
            return True
        except:
            return False

    # 检查文件类型
    def __check_file_type(self,File_path:Path) -> bool:
        if File_path.suffix == ".txt":
            self.__File_path_str : str = File_path
            self.__File_save_path_str : str = str(File_path)[:str(File_path).find(".")]+ ".mp3"
            self.__txt_data()
            return True
        else:
            raise "Only support：txt"
            return False

    # 检查文件是否合法
    def __check_file_path(self,File_path:str) -> bool:
        Path_File_path : Path = Path(File_path)
        if Path_File_path.is_file() and self.__check_file_type(Path_File_path):
            return True
        else:
            raise "File Not Find!!!"
            return False

    # 检查音频文件保存路径是否合法，及生成合法路径
    def __check_file_save_path(self,File_save_path:str) -> bool:
        if Path(File_save_path).exists():
            if Path(File_save_path).is_dir():
                self.__File_save_path_str : str = File_save_path+"/"+self.__File_save_path_str
            else:
                self.__File_save_path_str : str = File_save_path
            return True
        else:
            if -1 in [File_save_path.find("/"),File_save_path.find("\\")]:
                if File_save_path.find(".mp3") != -1:
                    self.__File_save_path_str : str = File_save_path
                else:
                    self.__File_save_path_str : str = File_save_path+".mp3"
                return True
            elif File_save_path.find(".mp3") != -1:
                self.__File_save_path_str : str = File_save_path
                return True
            else:
                raise "Directory Not Find!!!"
                return False

    # 检查音频文件配置信息是否合法，及生成合法配置
    def __check_option(self,Option) -> bool:
        try:
            sdp_pit = lambda x: x >= 0 and x <= 9
            vol = lambda x: x >= 0 and x <= 15
            per = lambda x: x >= 0 and x <= 5
            try:
                if sdp_pit(Option['spd']):
                    self.__Mp3_Option_dict['spd'] : int = Option['spd']
                elif Option['spd'] < 0:
                    print("spd < 0 default spd = 0")
                    self.__Mp3_Option_dict['spd'] : int = 0
                elif Option['spd'] > 9:
                    print("spd > 9 default spd = 9")
                    self.__Mp3_Option_dict['spd'] : int = 9
            except:
                self.__Mp3_Option_dict['spd'] : int = 5
            try:
                if sdp_pit(Option['pit']):
                    self.__Mp3_Option_dict['pit'] : int = Option['pit']
                elif Option['pit'] < 0:
                    print("pit < 0 default pit = 0")
                    self.__Mp3_Option_dict['pit'] : int = 0
                elif Option['pit'] > 9:
                    print("pit > 9 default pit = 9")
                    self.__Mp3_Option_dict['pit'] : int = 9
            except:
                self.__Mp3_Option_dict['pit'] : int = 5
            try:
                if vol(Option['vol']):
                    self.__Mp3_Option_dict['vol'] : int = Option['vol']
                elif Option['vol'] < 0:
                    print("vol < 0 default vol = 0")
                    self.__Mp3_Option_dict['vol'] : int = 0
                elif Option['vol'] > 15:
                    print("vol > 15 default vol = 15")
                    self.__Mp3_Option_dict['vol'] : int = 15
            except:
                self.__Mp3_Option_dict['vol'] : int = 5
            try:
                if per(Option['per']):
                    self.__Mp3_Option_dict['per'] : int = Option['per']
                elif Option['per'] < 0:
                    print("per < 0 default per = 0")
                    self.__Mp3_Option_dict['per'] : int = 0
                elif Option['per'] > 5:
                    print("per > 5 default per = 5")
                    self.__Mp3_Option_dict['per'] : int = 5
            except:
                self.__Mp3_Option_dict['per'] : int = 0
            return True
        except:
            raise "Option Error True:{'spd':0-9,'pit':0-9,'vol':0-15,'per':0-5} This Option is Negligible!!!"

    # 生成进度
    def __progress_bar(self) -> bool:
        centage : float = self.__Progress_bar_int / self.__Text_data_len
        bar : str = ''.join('=' * int(centage * 15))
        bar : str = '\r' + bar.ljust(15) + ' {:0>4.1f}%|100%'.format(centage * 100)
        print(bar,end='',flush=True)
        if centage == 1:
            print(bar,flush=True)
            return True
        return False

    # 处理文本文件
    def __txt_data(self) -> bool:
        try:
            with open(self.__File_path_str,"rb") as f:
                data : list = f.readlines()
                f.close()
            text_list : list = list()
            for i in data:
                temp : str = i.decode("utf-8")
                if len(temp) > 1024:
                    index : int = 0
                    for q in range(1,(len(temp) // 1024) + 1):
                        text_list.append(temp[index:index + (1023 * q)])
                        index += 1023 * q
                else:
                    text_list.append(i)
            for i in range(len(text_list)):
                self.__Text_data_dict[i] : str = text_list[i]
            return True
        except:
            raise "Text data encode not is utf-8"

    # 提交文本，生成音频文件
    def __post_data(self,index:int) -> bool:
        temp = self.__Baidu_connection.synthesis(self.__Text_data_dict[index],'zh',1,self.__Mp3_Option_dict)
        self.__Mp3_list.append(temp) if not isinstance(temp,dict) else self.__Mp3_Error_list.append(self.__Text_data_dict[index])
        self.__Progress_bar_int += 1
        return True

    # 设置提交文本配置
    def __post_data_set(self,is_Open_Threading:bool) -> bool:
        self.__Text_data_len : int = len(self.__Text_data_dict)
        if is_Open_Threading:
            Thread_list = list()
            for i in range(len(self.__Text_data_dict)):
                td = Thread(target=self.__post_data,args=(i,))
                Thread_list.append(td)
            for i in Thread_list:
                i.start()
            while True:
                if self.__progress_bar():
                    break
        else:
            for i in range(len(self.__Text_data_dict)):
                self.__post_data(i)
                self.__progress_bar()
            if self.__Mp3_Error_list != []:
                print("Have "+str(len(self.__Mp3_Error_list))+" Error\nuse：.getErrorList")
        return True

    # 保存音频文件
    def __save_data(self) -> str:
        try:
            with open(self.__File_save_path_str,"wb") as f:
                for i in self.__Mp3_list:
                    f.write(i)
                f.close()
                print("File Save Success!!!\nFile Path : "+self.__File_save_path_str)
                return self.__File_save_path_str
        except:
            raise "File Save Error!!!"

    # 返回生成失败的文本列表
    def getErrorList(self) -> list:
        return self.__Mp3_Error_list

    # 管理配置生成音频所需开关
    def getMp3(self,File_path:str,File_save_path = None,is_Open_Threading = False,Option = None) -> bool:
        if self.__isConnect_bool:
            if self.__check_file_path(File_path):
                if isinstance(Option,dict):
                    self.__check_option(Option)
                if File_save_path != None:
                    self.__check_file_save_path(File_save_path)
                self.__post_data_set(is_Open_Threading)
                self.__save_data()
                return True
        else:
            raise self.__Connect_error_str
            return False