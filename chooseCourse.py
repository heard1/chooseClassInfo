import requests
from datetime import datetime
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import re

sender = 'lsc@server1.com'
receivers = ['568497207@qq.com']

def mail(i,j,k):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(i+' '+j+'\n'+k, 'plain', 'utf-8')
    
    message['From'] = Header("server", 'utf-8')    # 发送者
    message['To'] =  Header("lsc", 'utf-8')        # 接收者
     
    subject = '可以选课啦'
    message['Subject'] = Header(subject, 'utf-8')


    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())




r = requests.get("http://jwbinfosys.zju.edu.cn/jwggcx.aspx?type=1")
soup = BeautifulSoup(r.text,"lxml")

info = []
infoTime = []
url=[]

for i in soup.findAll("tr"):
    count = 0
    for j in i.descendants:
        if count == 2:
            url.append(j)
        if count == 4:
            info.append(j.string)
        if count == 7:
            infoTime.append(j.string)
        #print(count,j)
        count+=1

url = url[1:-1]
info = info[1:-1]
infoTime = infoTime[1:-1]
infoTime = [ x[:10] for x in infoTime ]

a = re.compile(r'http.*?\'')
url = [a.findall(str(x))[0][:-1] for x in url]

today = datetime.now().strftime("%Y-%m-%d")

for (i,j,k) in zip(info,infoTime,url):
    if "选课" in i and j == today:
        mail(i,j,k)