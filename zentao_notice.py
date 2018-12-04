from requests_html import HTMLSession
import hashlib
import requests, os

productid = os.getenv("productid", "9")

session = HTMLSession()

host = "http://183.131.202.93:9090"

z = session.request(url=host + "/zentao/index.php?m=user&f=login", method="get")
verifyRand = z.html.find("input#verifyRand")[0].attrs["value"]
print("随机数:%s" % verifyRand)


def getMd5(s):
    h = hashlib.md5()
    h.update(s.encode("utf-8"))
    return h.hexdigest()


pwd = getMd5(getMd5("wujingjing123456") + verifyRand)
print("密码:%s" % pwd)

data = {
    "account": "wujingjing",
    "password": pwd,
    "keepLogin[]": "on"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# 登陆
zentao = session.request(url=host + "/zentao/index.php?m=user&f=login", method="post", data=data, headers=headers)

# 搜索
m = session.request(
    url=host + "/zentao/index.php?m=bug&f=browse&productid=" + productid + "&branch=0&browseType=unclosed",
    method="get")
# print(m.text)
print("*********************************************")

data1 = {
    "charts[]": "bugsPerAssignedTo",
}
report = session.request(
    url=host + "/zentao/index.php?m=bug&f=report&productID=" + productid + "&browseType=unclosed&branchID=0&moduleID=0",
    method="post", headers=headers, data=data1)
# print("bug报表:%s" % report.text)

names = report.html.find("td.chart-label")
bugs = report.html.find("td.chart-value")

bugCount = 0

result = {}

for name, bug in dict(zip(names, bugs)).items():
    if name.text in ["吴晶晶", "龚晓燕"]:
        continue
    result.update({
        name.text: bug.text
    })
    bugCount += int(bug.text)

s = ""
for k, v in result.items():
    s += "@" + k + "：" + v + "，"

if bugCount != 0:
    
    msg = "禅道Bug通知官-小Q：\n今日剩余未解决BUG共" + str(bugCount) + "个，其中" + s[:-1] + "\n谢谢开发童鞋！\(^o^)/  "

    print(msg)

    # 钉钉机器人
    WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN","https://oapi.dingtalk.com/robot/send?access_token=ae0cac2fe7b6685b19e372e7b571662c65ba301af283e6f0a576ec55403a09f7")

    textMsg = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": True
        }
    }

    res = requests.post(WEBHOOK_TOKEN, json=textMsg)
    print("钉钉发送成功！\n" + str(res.json()))
else:
    print("今日无bug！开森")
