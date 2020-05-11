#-*- coding:utf-8 -*-
import requests
import base64
import json
import os
import time


url="http://a.nuist.edu.cn/index.php/index/login"
file_path=os.path.dirname(__file__)
print(file_path)
data={'username':"",'password':"",'enablemacauth':'0',"domain":"NUIST"}
domain_codes={
    "1":"NUIST",
    "2":"CMCC",
    "3":"ChinaNet",
    "4":"Unicom"
}

class ByteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


def logo():
    print("""
      ____  _               _     _          _  __ _ 
     / ___|| |_ _   _ _ __ (_) __| |_      _(_)/ _(_)
     \___ \| __| | | | '_ \| |/ _` \ \ /\ / / | |_| |
      ___) | |_| |_| | |_) | | (_| |\ V  V /| |  _| |
     |____/ \__|\__,_| .__/|_|\__,_( )_/\_/ |_|_| |_|
                     |_|           |/                
                              --code by cc|needhourger
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         修改账户数据请删除本软件同目录下的config文件  
    """)


def inputData():
    global data

    print("请输入您的账户信息:")
    username=input("用户名 ")
    password=input("密  码 ")
    password=base64.b64encode(password.encode("utf-8"))

    print("请选择你的认证域(Default:1)：\n 1.南京信息工程大学\n 2.中国移动\n 3.中国电信\n 4.中国联通")
    x=input("请输入你的选择:")

    data={'username':username,'password':password,'enablemacauth':'0'}
    data["domain"]=domain_codes.get(x,"NUIST")

    if authWifi():
        saveData()

def saveData():
    global data
    with open(os.path.join(file_path,"data.json"),"w",encoding="utf-8") as f:
        json.dump(data,f,cls=ByteEncoder)


def loadData():
    global data
    if not os.path.exists(os.path.join(file_path,"data.json")):
        return False
    with open(os.path.join(file_path,"data.json"),"r",encoding="utf-8") as f:
        data=json.load(f)
        return True
    return False

def authWifi():
    global data
    r=requests.post(url,data=data)
    res=json.loads(r.text)
    for k,v in res.items():
        print("\t{}:{}".format(k,v))
    if res.get("status",0)==1:
        return True
    return False


if  __name__== "__main__":
    logo()
    if not loadData():
        inputData()
    else:
        authWifi()
    

