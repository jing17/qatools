import requests
import base64
import os,sys

def send_wechat_msg(content):
    '''发送企业微信消息'''
    # 登录获取token
    CORPID = "ww32787bc44b4a4d40"
    CORPSECRECT = "YP_x8fvdG64kf7Tf8otUP0l2jUzZE-nFAxHRqEa1D8Q"
    BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(CORPID, CORPSECRECT)

    result = requests.get(BASE_URL)
    access_token = result.json()["access_token"]
    # print("access_token=", access_token)

    # 发送文本消息
    URL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(access_token)
    json = {
        "touser": "",
        "toparty": "2",
        "totag": "",
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
            "content": content
        },
        "safe": 0
    }
    requests.post(url=URL, json=json)

    print(content)


def getBuildResult(buildID, jobName):
    '''获取构建结果'''
    # 获取authorization
    # userId = "admin"
    # token = "b0b98629bf7e43df99cb39e5ec35936d"
    userId = "wjj"
    token = "qa123456"
    s = "{0}:{1}".format(userId, token)
    authorization = base64.b64encode(s.encode(encoding="utf-8"))

    # 调用Jenkins查看构建结果的api
    # url = "http://localhost:8080/job/{0}/{1}/api/json".format(jobName, buildID)
    url = "http://114.115.182.227:8080/jenkins/job/{0}/{1}/api/json?pretty=true".format(jobName, buildID)
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Basic " + authorization.decode()
    }
    result = requests.get(url=url, headers=headers)
    # print(result.text)
    print("#########url: ",url)
    result_json = result.json()
    fullDisplayName = result_json["fullDisplayName"]
    res = result_json["result"]
    content = "构建项目：{0}\n构建结果：{1}\n若失败请及时<a href=\"http://localhost:8080/job/{2}/{3}/console\">查看日志</a>！".format(
        fullDisplayName, res, jobName, buildID)
    return content


if __name__ == '__main__':
    jobName = os.getenv("jobName", "test")
    buildNum = os.getenv("buildNum", 2)
    projectID = os.getenv("projectID", "160")
    BUILD_USER = os.getenv("BUILD_USER","default")
    content = "构建者：" + str(BUILD_USER) + "\n" + "构建参数：{ProjectID:" + projectID + "}\n\n" + getBuildResult(buildNum, jobName)
    send_wechat_msg(content)
