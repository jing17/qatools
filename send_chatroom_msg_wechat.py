import itchat
from itchat.content import *
import os
import requests
import base64


def send_msg(gname, context):
    '''个人微信给群组发送消息'''
    # 获取所有群的相关信息，update=True表示信息更新
    myroom = itchat.get_chatrooms(update=True)
    # print(myroom)
    global username

    # 搜索群名
    myroom = itchat.search_chatrooms(name=gname)
    # print("#########################")
    # print(myroom)
    for room in myroom:
        # print("###################################")
        # print(room)
        if gname in room['NickName']:
            username = room['UserName']
            itchat.send_msg(context, username)
        else:
            print('No groups found')
    print(context)


def getBuildResult(buildID, jobName):
    '''获取构建结果'''
    # 获取authorization
    userId = "admin"
    token = "b0b98629bf7e43df99cb39e5ec35936d"
    s = "{0}:{1}".format(userId, token)
    authorization = base64.b64encode(s.encode(encoding="utf-8"))

    # 调用Jenkins查看构建结果api
    url = "http://localhost:8080/job/{0}/{1}/api/json".format(jobName, buildID)
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Basic " + authorization.decode()
    }
    result = requests.get(url=url, headers=headers)
    # print(result.text)
    result_json = result.json()
    fullDisplayName = result_json["fullDisplayName"]
    res = result_json["result"]

    content = "构建项目：{0}\n构建结果：{1}\n若失败请及时查看日志：http://localhost:8080/job/{2}/{3}/console".format(
        fullDisplayName, res, jobName, buildID)
    return content


# # 监听是谁给我发消息（单人）
# @itchat.msg_register(INCOME_MSG)
# def text_reply(msg):
#     # 打印获取到的信息
#     print(msg)
#     itchat.send("微信目前处于python托管，你的消息我稍后查看，谢谢", toUserName=msg['FromUserName'])


# 监听是谁给我发消息（群聊）
# @itchat.msg_register(INCOME_MSG, isGroupChat=True)
# def text_reply(msg):
#     # 打印获取到的信息
#     print(msg)
#     itchat.send("微信目前处于python托管，你的消息我稍后查看，谢谢", toUserName=msg['FromUserName'])


if __name__ == '__main__':
    gname = '明明是美女团嘛'
    # context = '只是测试一下自动发送群组消息，大家可以忽略'

    jobName = os.getenv("jobName", "raptoapi")
    buildNum = os.getenv("buildNum", 5)
    projectID = os.getenv("projectID", "160")
    BUILD_USER = os.getenv('BUILD_USER', '吴晶晶')
    content = "构建者：" + BUILD_USER + "\n" + "构建参数\nProjectID：" + projectID + "\n\n" + getBuildResult(buildNum, jobName)

    itchat.auto_login(enableCmdQR=True, hotReload=True)
    send_msg(gname, content)
    itchat.run()
