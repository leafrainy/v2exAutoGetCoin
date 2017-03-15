#coding:utf8
# v2ex登录领金币
# 2017-03-15
# leafrainy (leafrainy.cc)  

from bs4 import BeautifulSoup as bs
import requests
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

#登录地址
mainUrl = "http://www.v2ex.com"
signinUrl = "http://www.v2ex.com/signin"
missionUrl = "https://www.v2ex.com/mission/daily/"

#登录账号信息
username = "m477927277"
password = "m477927277"

s = requests.Session()

#构造header头
headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',  
    'Origin': mainUrl,  
    'Referer': signinUrl,  
    'Host': 'www.v2ex.com',  
}

#用户名登录
signinData = s.get(signinUrl, headers=headers)  
signinContent = bs(signinData.content,'lxml')

#获取登录的动态信息
once = signinContent.find('input', {'name': 'once'})['value']
u = signinContent.find('input',{'class':'sl','type':'text'})['name']
p = signinContent.find('input',{'class':'sl','type':'password'})['name']

loginInfo = {u: username, p: password, 'once': once, 'next': '/'}  

#执行登录动作
loginData=s.post(signinUrl, loginInfo, headers=headers) 

#判断是否登录成功
indexData = s.get(mainUrl, headers=headers)  

loginName = bs(indexData.content,'lxml').find('span').get_text()

if loginName == username:
	print "登陆成功"
else:
	print "登录失败"
	exit(0)

#领取金币	
missionData = s.get(missionUrl,headers=headers)
coinStr= ((bs(missionData.content,'lxml').find('input',{'class':'super'})['onclick']).split('=',1)[1].split("'"))[1]
coinUrl = mainUrl+coinStr
coinData = s.get(coinUrl,headers=headers)
coninGetStatus = bs(coinData.content,'lxml').find('span',{'class':'gray'}).get_text()
if coninGetStatus.decode("utf-8") == "当前账户余额".decode("utf-8"):
	print "金币已领取，不要贪心哦~"
else:
	print coninGetStatus
	