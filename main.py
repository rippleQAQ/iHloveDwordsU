from getpass import getpass
from getToken import token
import requests
import uuid
import json
import time

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

def answerPaper(X_Auth_Token, mode, week, answerTime,precise):
    if precise == 1:
        paper = getData(X_Auth_Token, mode, week)
        paperID = paper['paperId']
        time.sleep(answerTime * 60)  # 测试时可关闭,正式使用时请打开
        test = paper["list"]
        answerList = []
        for i in range(100):
            title = test[i]["title"].split(' ')[0]
            answerA = test[i]["answerA"].split(' ')[0]
            answerB = test[i]["answerB"].split(' ')[0]
            answerC = test[i]["answerC"].split(' ')[0]
            answerD = test[i]["answerD"].split(' ')[0]
            if title in ku.keys():
                if ku[title] == answerA:
                    answerList.append('A')
                elif ku[title] == answerB:
                    answerList.append('B')
                elif ku[title] == answerC:
                    answerList.append('C')
                elif ku[title] == answerD:
                    answerList.append('D')
                else:
                    print("有题库之外的题目:")
                    print(f"第{i + 1}题：")
                    print(title)
                    print("A:" + str(answerA))
                    print("B:" + str(answerB))
                    print("C:" + str(answerC))
                    print("D:" + str(answerD))
                    x = input('请手动输入（字母大写，其他符号默认为C）：')
                    if x in ['A', 'B', 'C', 'D']:
                        answerList.append(x)
                    else:
                        answerList.append('C')
            else:
                print("有题库之外的题目:")
                print(f"第{i+1}题：")
                print(title)
                print("A:"+ str(answerA))
                print("B:"+ str(answerB))
                print("C:"+ str(answerC))
                print("D:"+ str(answerD))
                x = input('请手动输入（字母大写，其他符号默认为C）：')
                if x in ['A','B','C','D']:
                    answerList.append(x)
                else:
                    answerList.append('C')

        with open('answerList', 'r') as f:
            answerSource = f.read()
            f.close()
        answerDic = json.loads(answerSource)
        answerDic['paperId'] = paper['paperId']
        for i in range(0, 100):
            answerDic['list'][i]['input'] = answerList[i]
            answerDic['list'][i]['paperDetailId'] = paper['list'][i]['paperDetailId']
        postData(json.dumps(answerDic), X_Auth_Token)

    else:
        paper = getData(X_Auth_Token, mode, week)
        paperID = paper['paperId']
        time.sleep(answerTime * 60)  # 测试时可关闭,正式使用时请打开
        test = paper["list"]
        answerList = []
        for i in range(100):
            title = test[i]["title"].split(' ')[0]
            answerA = test[i]["answerA"].split(' ')[0]
            answerB = test[i]["answerB"].split(' ')[0]
            answerC = test[i]["answerC"].split(' ')[0]
            answerD = test[i]["answerD"].split(' ')[0]
            if title in ku.keys():
                if ku[title] == answerA:
                    answerList.append('A')
                elif ku[title] == answerB:
                    answerList.append('B')
                elif ku[title] == answerC:
                    answerList.append('C')
                elif ku[title] == answerD:
                    answerList.append('D')
                else:
                    answerList.append('C')
            else:
                answerList.append('C')

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

def answerPaper_for_tiku(X_Auth_Token, mode, week):
    paper = getData(X_Auth_Token, mode, week)
    paperID = paper['paperId']
    with open('answerList', 'r') as f:
        answerSource = f.read()
        f.close()
    answerDic = json.loads(answerSource)
    answerDic['paperId'] = paper['paperId']
    for i in range(0, 100):
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
    ku = {}
    with open('new_ku.txt', 'r') as f:
        data = f.read()
        data = json.loads(data)
        ku = data
        f.close()
    username = input('请输入您的学号：')
    password = getpass('请输入您的密码：')
    print("题库基本全，不需要再爬取")
    flag = input('爬题库(0)/自测或考试(1):')
    if int(flag) == 1:  #自测或考试
        mode = input('请输入模式-自测(0)/考试(1)：')
        week = input('请输入第几周(数字)：')
        answerTime = input('请输入答题时间(整数)(单位/min)(建议7min)：')
        precise = input("是否开启准确模式(不在题库中的题目手动做答)(0:关闭 1：开启):")
        myToken = token(username, password)
        print(f"脚本将在{answerTime}分钟后正式启动，期间请勿关闭脚本")
        if int(precise) == 1:
            print("检测到您开启了准确模式，最终时间为上面答题时间加上手动做答的时间，两者之和务必不要超过8min")
            print(f"不在题库中的题目会在{answerTime}分钟后弹出，记得做完！！！且控制时间！！！")
        paperID = answerPaper(myToken, mode, week, int(answerTime),int(precise))
        #自测或考试完后顺便更新题库
        dic = get_tiku(myToken, paperID)
        dic_list = dic["list"]
        ku = {}
        with open("new_ku.txt", "r") as f:
            data = f.read()
            data = json.loads(data)
            ku = data
            f.close()

        for i in range(100):
            title = dic_list[i]["title"].split(' ')[0]
            if title not in ku.keys():
                answerID = dic_list[i]["answer"]
                answer = dic_list[i][f"answer{answerID}"].split(' ')[0]
                ku[title] = answer

        with open("new_ku.txt", "w") as f:
            f.write(json.dumps(ku))
            f.close()

    else:   #爬取题库
        mode = 0
        week = input('请输入第几周(数字)：')
        x = input('爬取题库次数(每爬一次要等待8min，自测模式爬取):')
        print("用自测暴力得到题库")
        myToken = token(username, password)
        for a in range(int(x)):
            paperID = answerPaper_for_tiku(myToken, mode, week)
            dic = get_tiku(myToken, paperID)
            dic_list = dic["list"]
            ku = {}
            with open("new_ku.txt", "r") as f:
                data = f.read()
                data = json.loads(data)
                ku = data
                f.close()

            for i in range(100):
                title = dic_list[i]["title"].split(' ')[0]
                if title not in ku.keys():
                    answerID = dic_list[i]["answer"]
                    answer = dic_list[i][f"answer{answerID}"].split(' ')[0]
                    ku[title] = answer

            with open("new_ku.txt", "w") as f:
                f.write(json.dumps(ku))
                f.close()
            time.sleep(480)
