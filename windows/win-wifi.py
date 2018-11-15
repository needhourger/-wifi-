# -*- coding:utf-8 -*-
import requests
import base64
import json
import os

#目标网址
url="http://a.nuist.edu.cn/index.php/index/login"
global data

def print_logo():
    os.system("cls")
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
    #获取账户信息
    print u"请输入您的账户信息:"
    
    #获取用户名
    print u"用户名：",
    username=raw_input()
    
    #获取认证域
    print u"请选择你的认证域(Default:1)：\n 1.南京信息工程大学\n 2.中国移动\n 3.中国电信\n 4.中国联通"
    print u"请输入你的选择:",
    x=raw_input()

    #获取密码
    print u"密码：",
    temp=raw_input()
    password=base64.b64encode(temp)
    
    #处理认证域
    data={'username':username,'password':password,'enablemacauth':'0'}
    #print(data)
    #os.system("pause")
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
        os.system("pause")
        exit()
    
    #保存数据
    with open("./config.json","w+") as f:
        json.dump(data,f)
        f.close()
        print u"数据已保存"
        os.system("pause")

#web登陆认证
def web_authentication():
    #print(data)
    #print(url)
    while True:
        try:
            print_logo()
            print("tring web authentication...")
            print("")
            r=requests.post(url,data=data)
            break
        except:
            continue
        
    info=r.json()
    for key in info:
        print key,':',info[key]
    os.system("pause")

#查看wifi是否已连接
def check_wifi():
    print "checking wifi connection..."
    ret=os.popen("netsh wlan show interface")
    content=ret.read()
    content=content.decode("gbk")
    #print(content)
    if u"开放式" in content and u"i-NUIST" in content:
        return True
    else:
        return False

#连接wifi
def connect_nuist():
    print("Connecting i-NUSIT...")
    ret=os.popen("netsh wlan show networks")
    content=ret.read()
    content=content.decode("gbk")
    #print content
    if not("i-NUIST" in content):
        print u"无法连接到wifi : i-NUIST"
        os.system("pause")
        exit(0)

    ret=os.popen("netsh wlan connect name=i-NUIST ssid=i-NUIST")
    content=ret.read()
    content=content.decode("gbk")
    #print(content)
    if u"没有分配给指定接口的配置文件" in content:
        print(u"第一次连接i-NUIST请手动连接wifi")
    else:
        print("Connecting success")
        


#主函数
#name=""
if __name__=="__main__":
    print_logo()
    if not(check_wifi()):
        connect_nuist()
    
    print_logo()    
    try:
        with open("./config.json",'r') as f:
            data=json.load(f)
            f.close()
    except:
        First_step()
    finally:
        print_logo()
        with open("./config.json",'r') as f:
            data=json.load(f)
            web_authentication()
            f.close()
