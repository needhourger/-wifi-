# -*- coding: UTF-8 -*- 
import requests,base64,json,os


def First_step():
    x=''
    username=''
    password=''
    print u"请先输入您的账户信息"
    print u"用户名：",
    username=raw_input()
    print u"密码：",
    temp=raw_input()
    password=base64.b64encode(temp)
    data={'username':username,'password':password,'enablemacauth':'0'}
    print u"请选择你的认证域：\n 1.南京信息工程大学\n 2.中国移动\n 3.中国联通\n 4.中国电信"
    print u"请输入您的选择：",
    x=raw_input()
    t=1
    if x[0]=='1':
        data['domain']='NUIST'
        t=0
    if x[0]=='2':
        data['domain']='CMCC'
        t=0
    if x[0]=='3':
        data['domain']='Unicom'
        t=0
    if x[0]=='4':
        data['domain']='ChinaNet'
        t=0
    if t:
        print u"读入错误"
        os.system("pause")
        exit()

    with open("./config.json",'w+') as f:
        json.dump(data,f)
        print u"数据已保存"
        os.system("pause")
        f.close()




url="http://a.nuist.edu.cn/index.php/index/login"
try:
    with open("./config.json",'r') as f:
        data=json.load(f)
except:
    First_step()
finally:
    with open("./config.json",'r') as f:
        data=json.load(f)
r=requests.post(url,data=data)
info=r.json()
for key in info:
    print key,':',info[key]
os.system("pause")
