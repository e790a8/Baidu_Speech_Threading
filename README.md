# 简单百度语音识别

<img src="https://www.python.org/static/img/python-logo@2x.png" width=150px hegiht=150px align=left title="Python 3.8.2" href="https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe">  

## 项目简介

​	提供一个简单的文字转语音接口，做一个轮子，可同时使用多个账号进行识别，提高效率。  

## 配置说明

> 本项目使用[百度智能云](https://login.bce.baidu.com/)的[语音识别API]("https://ai.baidu.com/tech/speech")  
> 使用前，请使用百度账号登录[百度智能云](https://login.bce.baidu.com/)  
> 创建应用，添加语音识别功能  
> ![image-20200517135924671](https://github.com/lisztomania-Zero/Baidu_Speech_Threading/blob/master/image/image-20200517135924671.png)  
> 得到AppID、API Key、Secret Key即可  

## 依赖安装

> pip install -r requriements.txt  

## 方法说明

+ 创建实例  

``` python
Baidu_speech(App_ID:str,API_Key:str,Sercret_Key:str)

App_ID : 应用App_ID
API_Key : 应用API_Key
Sercret_Key : 应用Sercret_Key
```

+ 获取MP3  

``` python
getMp3(File_path:str,File_save_path = None,is_Open_Threading = False,Option = None)

File_path : txt文件路径名称
File_save_path : MP3文件保存路径与名称，默认与txt文件同目录同名称
is_Open_Threading : 是否开启多线程，默认不开启
Option : MP3音频属性，默认{'spd':5,'pit':5,'vol':5,'per':0}
	范围：{'spd':0-9,'pit':0-9,'vol':0-15,'per':0-5}
    'spd' : 语速，取值 0-5
    'pit' : 音调，取值 0-5
    'vol' : 音量，取值 0-15
    'per' : 发音人，0为女声（默认）、1为男声、3为情感男、4为情感女   
```

+ 获取未成功的文字集合  

```python
getErrorList()
```

## 示例代码

``` python
import baidu_speech

App_ID = "" # 17xxxx0x
API_Key = ""    # xxxxv8lbtxxxxNQG4lhxxxx
Secret_Key = "" # xxxxDclQ4pUwxxxxQXHGcVISoxxxxxDx
test = baidu_speech.Baidu_speech(App_ID,API_Key,Secret_Key)
test.getMp3("test.txt")
# test.getMp3("test.txt","test.mp3",False,{"spd":5,"pit":5,"vol":5,"per":0})
```

## 效果展示

![image-20200517135924672](https://github.com/lisztomania-Zero/Baidu_Speech_Threading/blob/master/image/image-20200517135924672.png)