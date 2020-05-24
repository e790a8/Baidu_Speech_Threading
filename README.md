# 简单百度语音识别

<img src="https://www.python.org/static/img/python-logo@2x.png" width=150px hegiht=150px align=center title="Python 3.8.2" href="https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe">  

--------------

## 项目简介

> 提供一个简单的文本转音频、音频转文本、视频转音频、视频转文本接口，可同时使用多个账号进行识别，提高效率。  
> 感觉还可以的给个star，谢谢了！

## 配置说明

> 本项目使用[百度智能云](https://login.bce.baidu.com/)的[语音识别API]("https://ai.baidu.com/tech/speech")  
> 使用前，请使用百度账号登录[百度智能云](https://login.bce.baidu.com/)  
> 创建应用，添加语音识别功能  
> ![image-20200517135924671](https://github.com/lisztomania-Zero/Baidu_Speech_Threading/blob/master/image/image-20200517135924671.png)  
> 得到AppID、API Key、Secret Key即可  

## 依赖安装

> pip install -r requirements.txt  

## 方法说明

+ 创建实例  

  ``` python
  Baidu_speech(App_ID:str,API_Key:str,Sercret_Key:str)

  App_ID : 应用App_ID
  API_Key : 应用API_Key
  Sercret_Key : 应用Sercret_Key
  ```

+ 文本转音频

  ``` python
  get_Text_to_Mp3(File_path:str,File_save_path = None,is_Open_Threading = False,Option = None)

  File_path : txt文件路径名称
  File_save_path : MP3文件保存路径与名称，默认与txt文件同目录同名称
  is_Open_Threading : 是否开启多线程，默认不开启
  Option : 生成音频配置参数，默认{'spd':5,'pit':5,'vol':5,'per':0}
        范围 : {'spd':0-9,'pit':0-9,'vol':0-15,'per':0-5}
        'spd' : 语速，取值 0-5
        'pit' : 音调，取值 0-5
        'vol' : 音量，取值 0-15
        'per' : 发音人，0为女声（默认）、1为男声、3为情感男、4为情感女   
  ```

+ 获取未成功的文本集合  

  ```python
  getErrorList()
  ```

+ 视频转音频

  ```python
  get_Video_to_Audio(File_path : str,File_save_path : str = None,format : str = None)
    
  File_path : 视频文件路径名称，支持视频格式为：MP4、FLV、WEBM
  File_save_path : 音频保存路径，默认与视频文件同目录同名称
  format : 音频格式，默认MP3，可指定为MP3、WAV
  ```
+ 视频转文本

  ```python
  get_Video_to_Text(File_path : str,File_save_path : str = None,is_Open_Threading : bool = False,Option : dict = None)
  
  File_path : 视频文件路径名称，支持视频格式为：MP4、FLV、WEBM
  File_save_path :文本保存路径，默认与视频文件同目录同名称
  is_Open_Threading : 是否开启多线程，默认不开启
  Option : 视频属性配置参数，默认{'dev_pid':1537}
      普通话(纯中文识别) : {'dev_pid':1537}
      英语 : {'dev_pid':1737}
      粤语 : {'dev_pid':1637}
      四川话 : {'dev_pid':1837}
      普通话远场 : {'dev_pid':1936}
  ```

+ 音频转文本

  ```python
  get_Audio_to_Text(File_path : str,File_save_path : str = None,is_Open_Threading : bool = False,Option : dict = None)
  
  File_path : 音频路径，支持音频格式为：MP3、WAV
  File_save_path : 文本保存路径，默认与音频路径同目录同名称
  is_Open_Threading : 是否开启多线程，默认不开启
  Option : 音频属性配置参数，默认{'dev_pid':1537}
      普通话(纯中文识别) : {'dev_pid':1537}
      英语 : {'dev_pid':1737}
      粤语 : {'dev_pid':1637}
      四川话 : {'dev_pid':1837}
      普通话远场 : {'dev_pid':1936}
  ```

  

## 示例代码

``` python
import baidu_speech

App_ID = "" # 17xxxx0x
API_Key = ""    # xxxxv8lbtxxxxNQG4lhxxxx
Secret_Key = "" # xxxxDclQ4pUwxxxxQXHGcVISoxxxxxDx
test = baidu_speech.Baidu_speech(App_ID,API_Key,Secret_Key)
# test.getMp3("test.txt")
test.get_Text_to_Mp3("test.txt",is_Open_Threading=True)
# test.getMp3("test.txt","test.mp3",False,{"spd":5,"pit":5,"vol":5,"per":0})
```

## 效果展示

![image-20200517135924672](https://github.com/lisztomania-Zero/Baidu_Speech_Threading/blob/master/image/image-20200517135924672.png)