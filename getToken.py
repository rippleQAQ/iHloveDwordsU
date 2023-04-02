import requests
import re
import execjs

session = requests.session()
class extra:
    
    def working1(self,account,password):
        with open('./login.js','r',encoding='utf-8') as p:
            jscode = p.read()
        headers_get1={
            'Host': 'cas.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive', 
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Cache-Control': 'max-age=0',
        }
        url1 = 'https://cas.hdu.edu.cn/cas/login?state=&service=https://skl.hdu.edu.cn/api/cas/login?state=&index='

        res = session.get(url1, headers=headers_get1)
        
        lt_match = re.findall('<input type="hidden" id="lt" name="lt" value="(\S+)" />',res.text)
        execution_match = re.findall('<input type="hidden" name="execution" value="(\S+)" />',res.text)
        eventId_match = re.findall('<input type="hidden" name="_eventId" value="(\S+)" />',res.text)
        account_length = len(account)
        password_length = len(password)

        lt = lt_match[0]    
        data = account+password+lt
        rsa = execjs.compile(jscode).call('strEnc',data,'1','2','3') 
        ul = account_length   
        pl = password_length   
        execution = execution_match[0] 
        eventId = eventId_match[0] 

        data1 = {
            'rsa': rsa,
            'ul': ul,
            'pl': pl,
            'lt': lt,
            'execution': execution,
            '_eventId': eventId
        }

        #data1='rsa={}&ul={}&pl={}&lt={}&execution={}&_eventId={}'.format(rsa,ul,pl,lt,execution,eventId)

        headers1 ={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://cas.hdu.edu.cn/cas/login?state=&service=https://skl.hdu.edu.cn/api/cas/login?state=&index=',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://cas.hdu.edu.cn',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
        }
        
        res1 = session.post(url1, data=data1,headers=headers1,allow_redirects=False) #这里没加allow_redirects属性，导致一直200
        #print(res1.history)
        total = res1.headers
        #关于requests的使用说明可以参考这个网址:https://docs.python-requests.org/zh_CN/latest/user/quickstart.html
        return total

    def working2(self,url_2):
        headers2 = {
            'Host': 'skl.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://cas.hdu.edu.cn/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
        }

        res2 = session.get(url_2,headers=headers2,allow_redirects=False)
        return res2.headers

    def working3(self,url_3):
        headers3 = {
            'Host': 'cas.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://cas.hdu.edu.cn/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
        }
        res3 = session.get(url_3,headers=headers3,allow_redirects=False)
        return res3.headers

    def working4(self,url_4):
        headers4 = {
            'Host': 'skl.hdu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://cas.hdu.edu.cn/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
        }
        res4 = session.get(url_4,headers=headers4,allow_redirects=False)
        return res4.headers
def token(username, password):
    test = extra()
    res1 = test.working1(username,password)
    try:
        res2 = test.working2(res1['Location'])
    except:
        print('用户名或密码错误！！！！')
        exit()
    res3 = test.working3(res2['Location'])
    res4 = test.working4(res3['Location'])
    token = res4['X-Auth-Token']
    return token
     

     


    
