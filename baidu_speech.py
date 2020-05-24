#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/05/24
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : baidu_speech.py

from aip import AipSpeech
from pathlib import Path
from threading import Thread
from hashlib import md5
from platform import system
from pydub import AudioSegment
from os import remove

class Baidu_speech:
    # 是否连接成功
    __isConnect_bool : bool = False
    # MP3转码所需文件是否齐全
    __isFfmpeg_File_Hava : bool = False
    # 现在使用的功能
    __Now_use : int = None
    # 操作系统
    __System_name : str = None
    # 存储文本数据
    __Text_data_dict : dict = dict()
    # 音频文件保存路径
    __File_save_path_str : str = str()
    # 文本转音频文件配置信息
    __Mp3_Option_dict : dict = dict()
    # 音频转文本文件配置信息
    __Audio_Option_dict : dict = dict()
    # 成功的文本转音频片段
    __Mp3_list : list = list()
    # 失败的文本转音频片段
    __Mp3_Error_list : list = list()
    # 成功的音频转文本片段
    __Text_dict : dict = dict()
    # 失败的音频转文本片段
    __Text_Error_list : list = list()
    # 数据长度
    __Data_len : int = 0
    # 生成进度
    __Progress_bar_int : int = 0
    # 保存错误音频进度
    __Text_Error_progress_bar : int = 0
    # 音频文件拆分
    __AudioSegment_from_audio_dict : dict = dict()
    # 临时数据目录
    __temp_dir : Path = Path("temp")
    # 支持文本类型
    __Text_type : set = set([".txt"])
    # 支持音频类型
    __Audio_type : set = set([".mp3",".wav"])
    # 支持视频类型
    __Video_type : set = set([".mp4",".flv",".webm"])
    # 连接失败提示文本
    __Connect_error_str : str = "Connection Error Please Again Input!!!"

    # 初始化
    def __init__(self,app_id:str,api_key:str,secret_key:str):
        self.__App_ID : str = app_id
        self.__API_Key : str = api_key
        self.__Secret_Key : str = secret_key
        self.__System_name : str = system()
        self.__baidu_conn()

    # 连接
    def __baidu_conn(self) -> bool:
        self.__Baidu_connection :AipSpeech = AipSpeech(self.__App_ID,self.__API_Key,self.__Secret_Key)
        if self.__check_baidu_conn():
            print("Connection Success!!!")
            self.__isConnect_bool: bool = True
            return True
        else:
            self.__isConnect_bool : bool = False
            raise self.__Connect_error_str
            return False

    # 检查连接
    def __check_baidu_conn(self) -> bool:
        try:
            check = self.__Baidu_connection.synthesis("测试",'zh',1,{'vol':5})
            return True
        except:
            return False

    # 检查文件类型
    def __check_file_type(self,File_path:Path) -> bool:
        if self.__Now_use == 1:
            if File_path.suffix in self.__Text_type:
                self.__File_path_Path : str = File_path
                self.__File_save_path_str : str = File_path.name[:File_path.name.rfind(".")] + ".mp3"
                self.__txt_data()
                return True
            else:
                raise "Only support：txt"
        elif self.__Now_use == 2:
            if File_path.suffix in self.__Audio_type:
                self.__File_path_Path : Path = File_path
                self.__File_save_path_str : str = File_path.name[:File_path.name.rfind(".")] + ".txt"
                self.__audio_data()
                return True
            else:
                raise "Only support: mp3,wav"
        elif self.__Now_use in [3,4]:
            if File_path.suffix in self.__Video_type:
                self.__File_path_Path : Path = File_path
                if self.__Now_use == 4:
                    self.__File_save_path_str: str = File_path.name[:File_path.name.rfind(".")] + ".txt"
                else:
                    self.__File_save_path_str : str = File_path.name[:File_path.name.rfind(".")] + self.__Audio_format
                self.__video_data()
                return True
            else:
                raise "Only support:mp4,flv,webm"
        return False

    # 检查文件是否合法
    def __check_file_path(self,File_path:str) -> bool:
        Path_File_path : Path = Path(File_path)
        if Path_File_path.is_file() and self.__check_file_type(Path_File_path):
            return True
        else:
            raise "File Not Find!!!"
            return False

    # 检查文件保存路径是否合法，及生成合法路径
    def __check_file_save_path(self,File_save_path:str) -> bool:
        File_save_path : Path = Path(File_save_path)
        if File_save_path.name.rfind(".") != -1:
            File_save_path_name : str = File_save_path.name[:File_save_path.name.rfind(".")]
        else:
            File_save_path_name : str = File_save_path.name
        path: str = str(File_save_path)[:str(File_save_path).rfind("/")]
        path_1: str = str(File_save_path)[:str(File_save_path).rfind("\\")]
        if len(path) > len(path_1):
            path : Path = Path(path)
        else:
            path : Path = Path(path_1)
        if not path.is_dir():
            path : Path = Path("")
        if self.__Now_use == 1:
            suffix : str = ".mp3"
        elif self.__Now_use in [2,4]:
            suffix : str = ".txt"
        elif self.__Now_use == 3:
            suffix : str = self.__Audio_format
        if File_save_path.exists():
            if File_save_path.is_dir():
                self.__File_save_path_str : str = str(File_save_path)+"/"+self.__File_save_path_str
            elif File_save_path.suffix == suffix:
                self.__File_save_path_str : str = str(File_save_path)
            else:
                self.__File_save_path_str : str = str(path) + "/" + File_save_path_name + suffix
            return True
        else:
            if [str(File_save_path).find("/"),str(File_save_path).find("\\")].count(-1) == 2:
                if File_save_path.suffix == suffix:
                    self.__File_save_path_str : str = str(File_save_path)
                else:
                    self.__File_save_path_str : str = File_save_path_name + suffix
                return True
            else:
                if path.exists():
                    if File_save_path.suffix == suffix:
                        self.__File_save_path_str : str = str(File_save_path)
                    else:
                        self.__File_save_path_str : str = str(path) + "/" + File_save_path_name + suffix
                    return True
                else:
                    raise "Directory Not Find!!!"
                    return False

    # 检查文本转音频文件配置信息是否合法，及生成合法配置
    def __check_text_option(self,Option) -> bool:
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

    # 检查音频转文本文件配置信息是否合法，及生成合法配置
    def __check_audio_option(self,Option : dict) -> bool:
        dev_pid : list = [1537,1737,1637,1837,1936]
        try:
            if Option['dev_pid'] in dev_pid:
                    self.__Audio_Option_dict['dev_pid'] : int = Option['dev_pid']
            else:
                    self.__Audio_Option_dict['dev_pid'] : int = 1537
            return True
        except:
            raise "Option Error True:{'dev_pid':1537} ,dev_pid in [1537,1737,1637,1837,1936] This Option is Negligible!!!"

    # 检查ffmpeg所需的必须文件
    def __check_FFMPEG_EXE(self) -> bool:
        if self.__System_name == "Windows":
            ffmpeg_name : str = "ffmpeg.exe"
            ffplay_name : str = "ffplay.exe"
            ffprobe_name : str = "ffprobe.exe"
        else:
            raise "I'm Sorry.This feature is only supported for Windows for the time being"
        try:
            ffmpeg_md5 : str = md5()
            ffplay_md5 : str = md5()
            ffprobe_md5 : str = md5()
            try:
                with open(ffmpeg_name,"rb") as f:
                    for i in f.readlines():
                        ffmpeg_md5.update(i)
                    f.close()
            except:
                raise "Did not find " + ffmpeg_name
            try:
                with open(ffplay_name,"rb") as f:
                    for i in f.readlines():
                        ffplay_md5.update(i)
                    f.close()
            except:
                raise "Did not find " + ffplay_name
            try:
                with open(ffprobe_name,"rb") as f:
                    for i in f.readlines():
                        ffprobe_md5.update(i)
                    f.close()
            except:
                raise "Did not find " + ffprobe_name
            self.__isFfmpeg_File_Hava = ffmpeg_md5.hexdigest() == "f0b8d6979592dc04fcde332b00d636db"
            self.__isFfmpeg_File_Hava = ffplay_md5.hexdigest() == "072545168926d04c0fb19cf3cf907210"
            self.__isFfmpeg_File_Hava = ffprobe_md5.hexdigest() == "0f77d15b710f90e8bfe5ef91d41e2944"
            if not self.__isFfmpeg_File_Hava:
                raise "Files unknown"
            else:
                return True
        except:
            raise "Did not find all file!!"

    # 生成进度
    def __progress_bar(self) -> bool:
        centage : float = self.__Progress_bar_int / self.__Data_len
        bar : str = ''.join('=' * int(centage * 15))
        bar : str = '\r' + bar.ljust(15) + ' {:0>4.1f}%|100%'.format(centage * 100)
        print(bar,end='',flush=True)
        if centage == 1:
            print(bar,flush=True)
            self.__Progress_bar_int : int = 0
            return True
        return False

    # 处理视频文件
    def __video_data(self) -> bool:
        try:
            if self.__File_path_Path.suffix == ".flv":
                self.__AudioSegment_from_video : AudioSegment = AudioSegment.from_flv(self.__File_path_Path)
            else:
                self.__AudioSegment_from_video : AudioSegment = AudioSegment.from_file(self.__File_path_Path,format=self.__File_path_Path.suffix[1:])
        except:
            raise "Video Error"

    # 处理音频文件
    def __audio_data(self) -> bool:
        try:
            if self.__File_path_Path.suffix == ".mp3":
                self.__AudioSegment_from_audio : AudioSegment = AudioSegment.from_mp3(self.__File_path_Path)
            elif self.__File_path_Path.suffix == ".wav":
                self.__AudioSegment_from_audio : AudioSegment = AudioSegment.from_wav(self.__File_path_Path)
            self.__AudioSegment_from_audio: AudioSegment = self.__AudioSegment_from_audio.set_frame_rate(frame_rate=16000).set_channels(1)
            self.__break_up_audio()
            return True
        except:
            raise  "Audio Error"

    # 切割音频，将音频切割成59秒一段
    def __break_up_audio(self) -> bool:
        self.__temp_audio_dir : Path = Path(str(self.__temp_dir)+"/audio")
        if not self.__temp_audio_dir.is_dir():
            self.__temp_audio_dir.mkdir(parents = True)
        audio_list : list = list()
        if self.__AudioSegment_from_audio.duration_seconds > 59:
            index : int = 0
            audio_len : int = int((self.__AudioSegment_from_audio.duration_seconds * 1000) // 59000)
            for i in range(1,audio_len + 2):
                audio_list.append(self.__AudioSegment_from_audio[index:i * 59000])
                index = i * 59000
        else:
            audio_list.append(self.__AudioSegment_from_audio)
        for i in range(len(audio_list)):
            self.__AudioSegment_from_audio_dict[i] : AudioSegment = audio_list[i]
        self.__Data_len : int = len(self.__AudioSegment_from_audio_dict)
        Thread_list : list = list()
        for i in range(len(self.__AudioSegment_from_audio_dict)):
            td : Thread = Thread(target=self.__audio_to_bytes,args=(i,))
            Thread_list.append(td)
        for threading in Thread_list:
            threading.start()
        while True:
            if self.__Progress_bar_int == self.__Data_len:
                self.__Progress_bar_int : int = 0
                break
        return True

    # 将音频数据转为二进制数据
    def __audio_to_bytes(self,index) -> bool:
        temp_file_path :str = str(self.__temp_audio_dir)+"/"+str(index)+".wav"
        self.__AudioSegment_from_audio_dict[index].export(temp_file_path,format="wav")
        with open(temp_file_path,"rb") as audio_file:
            self.__AudioSegment_from_audio_dict[index] : bytes = audio_file.read()
            audio_file.flush()
            audio_file.close()
        remove(temp_file_path)
        self.__Progress_bar_int += 1
        return True

    # 处理文本文件
    def __txt_data(self) -> bool:
        try:
            with open(self.__File_path_Path,"rb") as f:
                data : list = f.readlines()
                f.close()
            text_list : list = list()
            for i in data:
                temp : str = i.decode("utf-8")
                if len(temp) > 1024:
                    index : int = 0
                    for q in range(1,(len(temp) // 1024) + 2):
                        text_list.append(temp[index:1023 * q])
                        index = 1023 * q
                else:
                    text_list.append(i)
            for i in range(len(text_list)):
                self.__Text_data_dict[i] : str = text_list[i]
            self.__Data_len: int = len(self.__Text_data_dict)
            return True
        except:
            raise "Text data encode not is utf-8"

    # 提交文本,生成音频文件
    def __post_text_data(self,index:int) -> bool:
        temp = self.__Baidu_connection.synthesis(self.__Text_data_dict[index],'zh',1,self.__Mp3_Option_dict)
        self.__Mp3_list.append(temp) if not isinstance(temp,dict) else self.__Mp3_Error_list.append(self.__Text_data_dict[index])
        self.__Progress_bar_int += 1
        return True

    # 设置提交文本配置
    def __post_text_data_set(self,is_Open_Threading:bool) -> bool:
        if is_Open_Threading:
            Thread_list = list()
            for i in range(len(self.__Text_data_dict)):
                td = Thread(target=self.__post_text_data,args=(i,))
                Thread_list.append(td)
            for i in Thread_list:
                i.start()
            while True:
                if self.__progress_bar():
                    break
        else:
            for i in range(len(self.__Text_data_dict)):
                self.__post_text_data(i)
                self.__progress_bar()
        if self.__Mp3_Error_list != []:
            print("Have "+str(len(self.__Mp3_Error_list))+" Error\nuse：.getErrorList")
        return True

    # 保存文本转音频的文件
    def __save_MP3_data(self) -> bool:
        try:
            with open(self.__File_save_path_str,"wb") as f:
                for i in self.__Mp3_list:
                    f.write(i)
                f.close()
                print("MP3 File Save Success!!!\nFile Path : "+self.__File_save_path_str)
                return True
        except:
            raise "MP3 File Save Error!!!"

    # 返回生成失败的文本列表
    def getErrorList(self) -> list:
        return self.__Mp3_Error_list

    # 管理配置生成音频所需开关
    def get_Text_to_Mp3(self,File_path:str,File_save_path = None,is_Open_Threading = False,Option = None) -> bool:
        if self.__isConnect_bool:
            self.__Now_use : int = 1
            if self.__check_file_path(File_path):
                if isinstance(Option,dict):
                    self.__check_text_option(Option)
                if File_save_path != None:
                    self.__check_file_save_path(File_save_path)
                self.__post_text_data_set(is_Open_Threading)
                self.__save_MP3_data()
                return True
        else:
            raise self.__Connect_error_str
            return False

    # 提交音频,生成文本文件
    def __post_audio_data(self,index:int) -> bool:
        temp = self.__Baidu_connection.asr(self.__AudioSegment_from_audio_dict[index],'wav',16000,self.__Audio_Option_dict)
        try:
            self.__Text_dict[index] : str = temp['result'][0]
        except:
            self.__Text_Error_list.append([index, self.__AudioSegment_from_audio_dict[index]])
        self.__Progress_bar_int += 1
        return True

    # 设置提交音频配置
    def __post_audio_data_set(self,is_Open_Threading:bool) -> bool:
        if is_Open_Threading:
            Thread_list = list()
            for index in range(len(self.__AudioSegment_from_audio_dict)):
                td = Thread(target=self.__post_audio_data,args=(index,))
                Thread_list.append(td)
            for threading in Thread_list:
                threading.start()
            while True:
                if self.__progress_bar():
                    break
        else:
            for audio_index in range(len(self.__AudioSegment_from_audio_dict)):
                self.__post_audio_data(audio_index)
                self.__progress_bar()
        if self.__Text_Error_list != []:
            self.__save_error_audio_set()
            print("Have " + str(len(self.__Text_Error_list)) + " Error\n Save:temp/Error/*.wav")
        return True

    # 时间计算
    def __time_conversion(self,index:int) -> str:
        time_temp : int = index * 59
        time_return : str = str()
        if time_temp // 86400 != 0:
            day = time_temp // 86400
            time_temp -= 86400 * day
            if len(str(day)) == 1:
                day = '0' + str(day)
            else:
                day = str(day)
            time_return += day + "-"
        if time_temp // 3600 != 0:
            hours = time_temp // 3600
            time_temp -= 3600 * hours
            if len(str(hours)) == 1:
                hours = '0' + str(hours)
            else:
                hours = str(hours)
            time_return += hours + "-"
        if time_temp // 60 != 0:
            minutes = time_temp // 60
            time_temp -= 60 * minutes
            if len(str(minutes)) == 1:
                minutes = '0' + str(minutes)
            else:
                minutes = str(minutes)
            time_return += minutes + "-"
        seconds = time_temp
        if len(str(seconds)) == 1:
            seconds = '0' + str(seconds)
        else:
            seconds = str(seconds)
        time_return += seconds
        return time_return

    # 保存转换失败的音频片段配置
    def __save_error_audio_set(self) -> bool:
        self.__temp_audio_error_dir : Path = Path(str(self.__temp_dir)+"/error_audio")
        if not self.__temp_audio_error_dir.is_dir():
            self.__temp_audio_error_dir.mkdir(parents=True)
        Thread_list : list = list()
        for error_audio in self.__Text_Error_list:
            td = Thread(target=self.__save_error_audio,args=(error_audio,))
            Thread_list.append(td)
        for threading in Thread_list:
            threading.start()
        Text_Error_list_len = len(Thread_list)
        while True:
            if self.__Text_Error_progress_bar == Text_Error_list_len:
                self.__Text_Error_progress_bar : int = 0
                break
        return True

    # 保存转换失败的音频片段
    def __save_error_audio(self,error_audio) -> bool:
        start_time : str = self.__time_conversion(error_audio[0])
        end_time : str = self.__time_conversion(error_audio[0] + 1)
        file_name : str = str(self.__temp_audio_error_dir) + "/" + start_time + "——" + end_time + ".wav"
        with open(file_name, "wb") as audio_error:
            audio_error.write(error_audio[1])
            audio_error.flush()
            audio_error.close()
        self.__Text_Error_progress_bar += 1
        return True

    # 保存音频转文本的文本
    def __save_text_data(self) -> bool:
        try:
            with open(self.__File_save_path_str,"w",encoding="utf-8") as text_file:
                for text_index in range(self.__Data_len):
                    try:
                        text_file.write(self.__Text_dict[text_index])
                    except:
                        text_file.write("---------")
                text_file.flush()
                text_file.close()
            print("Text File Save Success!!!\nFile Path : " + self.__File_save_path_str)
            return True
        except:
            raise "Text File Save Error!!!"

    # 管理配置生成文本所需开关
    def get_Audio_to_Text(self,File_path : str,File_save_path : str = None,is_Open_Threading : bool = False,Option : dict = None) -> bool:
        if self.__isConnect_bool:
            self.__Now_use : int = 2
            if self.__check_FFMPEG_EXE():
                if self.__check_file_path(File_path):
                    if isinstance(Option,dict):
                        self.__check_audio_option(Option)
                    if File_save_path != None:
                        self.__check_file_save_path(File_save_path)
                    self.__post_audio_data_set(is_Open_Threading)
                    self.__save_text_data()
                    return True
        else:
            raise self.__Connect_error_str
            return False

    # 保存视频转音频的文件
    def __save_audio_data(self) -> bool:
        self.__AudioSegment_from_video.export(self.__File_save_path_str,format=self.__Audio_format[1:])
        return True

    # 视频转音频
    def get_Video_to_Audio(self,File_path : str,File_save_path : str = None,format : str = None) -> str:
        self.__Now_use : int = 3
        if self.__check_FFMPEG_EXE():
            if format != None:
                format = format.lower()
                if "." + format in self.__Audio_type:
                    self.__Audio_format : str = "." + format
                else:
                    self.__Audio_format : str = ".mp3"
            else:
                self.__Audio_format : str = ".mp3"
            if self.__check_file_path(File_path):
                if File_save_path != None:
                    self.__check_file_save_path(File_save_path)
                self.__save_audio_data()
                print("Audio Path:"+self.__File_save_path_str)
                return self.__File_save_path_str
        else:
            return None

    # 视频转文本
    def get_Video_to_Text(self,File_path : str,File_save_path : str = None,is_Open_Threading : bool = False,Option : dict = None) -> str:
        self.__Now_use : int = 4
        if self.__check_FFMPEG_EXE():
            if self.__check_file_path(File_path):
                if File_save_path != None:
                    self.__check_file_save_path(File_save_path)
                File_save_path : str = self.__File_save_path_str
                if Option != None:
                    self.__check_audio_option(Option=Option)
            self.get_Video_to_Audio(self.__File_path_Path)
            remove_file_path : str = self.__File_save_path_str
            self.get_Audio_to_Text(self.__File_save_path_str,File_save_path,is_Open_Threading=is_Open_Threading,Option=self.__Audio_Option_dict)
            remove(remove_file_path)
            return self.__File_save_path_str
        else:
            return None