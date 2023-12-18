from getpass import getpass
from getToken import token
import requests
import uuid
import json
import time
import random

def getData(x_token, mode, week):
    # 获取当前时间戳
    timestamp = int(time.time() * 10000)
    getUrl = f'https://skl.hdu.edu.cn/api/paper/new?type={mode}&week={week}&startTime='+ str(
        timestamp)  # 这里参数type中0为自测,1为考试。week参数为第几周。
    getHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # 获取当前uuid（测试发现是uuid1）
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 13; zh-CN; V2203A Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.1.255 Mobile Safari/537.36 AliApp(DingTalk/7.0.15) com.alibaba.android.rimet/28810254 Channel/700159 language/zh-CN abi/64 colorScheme/dark;',
        # 自己的token
        'X-Auth-Token': x_token
    }
    response = requests.get(getUrl, headers=getHeaders)
    return json.loads(response.text)


def postData(answer, x_token):
    url = 'https://skl.hdu.edu.cn/api/paper/save'

    postHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 13; zh-CN; V2203A Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.1.255 Mobile Safari/537.36 AliApp(DingTalk/7.0.15) com.alibaba.android.rimet/28810254 Channel/700159 language/zh-CN abi/64 colorScheme/dark;',
        'X-Auth-Token': x_token
    }
    requests.post(url, headers=postHeaders, data=answer)

def answerPaper(X_Auth_Token, mode, week, answerTime,score):
    cnt = 0
    rand = []
    paper = getData(X_Auth_Token, mode, week)
    paperID = paper['paperId']
    test = paper["list"]
    while answerTime>1: # 测试时可关闭,正式使用时请打开
        print('\r' + ' ' * 50 + '\r', end='', flush=True)
        print("剩余",answerTime,"秒", end='', flush=True)
        answerTime=answerTime-1
        time.sleep(1)
    time.sleep(answerTime)
    print()
    answerList = []
    index = ['A','B','C','D']
    for i in range(100):
        title = test[i]["title"].split(' ')[0]
        answerA = test[i]["answerA"].split(' ')[0]
        answerB = test[i]["answerB"].split(' ')[0]
        answerC = test[i]["answerC"].split(' ')[0]
        answerD = test[i]["answerD"].split(' ')[0]
        if [title,answerA] in ku:
            answerList.append('A')
        elif [title,answerB] in ku:
            answerList.append('B')
        elif [title,answerC] in ku:
            answerList.append('C')
        elif [title,answerD] in ku:
            answerList.append('D')
        else:
            answerList.append('C')
            cnt+=1

    if 100 - cnt > score:
        a = 100 - cnt - score
        while len(rand) < a:
            x = random.randint(0, 99)
            if x not in rand:
                rand.append(x)

        for j in rand:
            y = random.choice(index)
            while y == answerList[j]:
                y = random.choice(index)
            answerList[j] = y

    with open('answerList', 'r') as f:
        answerSource = f.read()
        f.close()
    answerDic = json.loads(answerSource)

    answerDic['paperId'] = paper['paperId']
    for i in range(0, 100):
        answerDic['list'][i]['input'] = answerList[i]
        answerDic['list'][i]['paperDetailId'] = paper['list'][i]['paperDetailId']
    postData(json.dumps(answerDic), X_Auth_Token)

    return paperID

def get_tiku(x_token, ID):
    getUrl = f'https://skl.hdu.edu.cn/api/paper/detail?paperId={ID}'
    getHeaders = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'skl.hdu.edu.cn',
        'Origin': 'https://skl.hduhelp.com',
        'Pragma': 'no-cache',
        'Referer': 'https://skl.hduhelp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # 获取当前uuid（测试发现是uuid1）
        'skl-ticket': str(uuid.uuid1()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        # 自己的token
        'X-Auth-Token': x_token
    }
    response = requests.get(getUrl, headers=getHeaders)
    return json.loads(response.text)

if __name__ == '__main__':
    with open('new_ku_list.txt', 'r') as f:
        data = f.read()
        data = json.loads(data)
        ku = data
        f.close()
    username = input('请输入您的学号:')
    password = getpass('请输入您的密码:')

    mode = input('请输入模式-自测(0)/考试(1):')
    week = input('请输入第几周(数字)(经测试只能做本周的题目,输入对应周即可):')
    print("为避免误输入,答题时间在120~480范围外的默认随机生成120~480间的一个数")
    print("不输入表示生成一个120~480范围的随机数")
    answerTime = input('请输入答题时间(整数,注意单位为秒！)(单位/s):')
    if answerTime == '':
        answerTime = random.randint(120,480)
    else:
        answerTime = int(answerTime)
        if answerTime>480 or answerTime<120:
            answerTime = random.randint(120,480)
    print("\n为避免误输入,分数在0~100范围外的默认随机生成90~98间的一个数")
    score = input('请输入你想要的分数(结果可能稍有偏差),不输入默认随机生成90~98:')
    if score == '':
        score = random.randint(90,98)
    else:
        score = int(score)
        if score < 0 or score > 100:
            score = random.randint(90,98)
    myToken = token(username, password)
    print(f"脚本将在{answerTime}秒后正式启动,期间请勿关闭脚本")
    paperID = answerPaper(myToken, mode, week, answerTime,score)
    #自测或考试完后顺便更新题库
    dic = get_tiku(myToken, paperID)
    dic_list = dic["list"]
    with open("new_ku_list.txt", "r") as f:
        data = f.read()
        data = json.loads(data)
        ku = data
        f.close()

    for i in range(100):
        title = dic_list[i]["title"].split(' ')[0]
        answerID = dic_list[i]["answer"]
        answer = dic_list[i][f"answer{answerID}"].split(' ')[0]
        li = [title,answer]
        if li not in ku:
                ku.append(li)

    with open("new_ku_list.txt", "w") as f:
        f.write(json.dumps(ku))
        f.close()

    print("脚本结束,将在10秒后自动退出")
    time.sleep(10)
