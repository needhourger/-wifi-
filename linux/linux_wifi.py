#-*- coding:utf-8 -*-
import requests
import base64
import json
import os
import time


url="http://a.nuist.edu.cn/index.php/index/login"
global data

file_path=os.path.dirname(os.path.abspath(__file__))

def print_log():
    os.system("clear")
    print"  ____  _               _     _          _  __ _ "
    print" / ___|| |_ _   _ _ __ (_) __| |_      _(_)/ _(_)"
    print" \___ \| __| | | | '_ \| |/ _` \ \ /\ / / | |_| |"
    print"  ___) | |_| |_| | |_) | | (_| |\ V  V /| |  _| |"
    print" |____/ \__|\__,_| .__/|_|\__,_( )_/\_/ |_|_| |_|"
    print"                 |_|           |/                "
    print"                          --code by cc|needhourger"
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(u" 修改账户数据请删除本软件同目录下的config文件  ")
    print("")


def First_step():
    x=""
    username=""
    password=""
    data={}

    print u"请输入您的账户信息:"

    print u"用户名:",
    username=raw_input()

    print u"请选择你的认证域(Default:1)：\n 1.南京信息工程大学\n 2.中国移动\n 3.中国电信\n 4.中国联通"
    print u"请输入你的选择:",
    x=raw_input()

    print u"密码：",
    temp=raw_input()
    password=base64.b64encode(temp)

    data={'username':username,'password':password,'enablemacauth':'0'}

    if x=="":
        x="1"
    if x[0]=='1':
        data['domain']='NUIST'
    elif x[0]=='2':
        data['domain']='CMCC'
    elif x[0]=='3':
        data['domain']='ChinaNet'
    elif x[0]=='4':
        data['domain']='Unicom'
    else:
        print u"读入错误"
        time.sleep(3)
        exit()

    with open(file_path+"/config.json","w+") as f:
        json.dump(data,f)
        f.close()
        print u"数据已保存"
        time.sleep(1.5)

def web_authentication():
    #print(data)
    #print(url)
    while True:
        try:
            print_log()
            print("tring web authentication...")
            print("")
            r=requests.post(url,data=data)
            break
        except:
            continue
        
    info=r.json()
    for key in info:
        print key,':',info[key]

#name=""
if  __name__== "__main__":
    print_log()
    try:
        with open(file_path+"/config.json","r") as f:
            data=json.load(f)
            f.close()
    except:
        First_step()
    finally:
        print_log()
        with open(file_path+"/config.json","r") as f:
            data=json.load(f)
            f.close()
            web_authentication()
