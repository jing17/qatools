import requests
from jinja2 import Template
import json

# 指定项目的所有测试脚本，可执行apiID（单个接口）
projectID = "15"
apiID = None

session = requests.session()
body = {
    "email": "wujingj@zjbdos.com",
    "password": "Jing2018"
}
# 登录
res = session.post("http://183.131.202.93:9071/api/user/login", json=body)


def getAPIList(projectID, catID, apiID=None, tag=None):
    '''
    获取指定条件下所有接口
    '''
    catList = session.get("http://183.131.202.93:9071/api/interface/list_menu?project_id=" + projectID).json()["data"]
    apiIDList = []
    if apiID != None:
        apiIDList.extend(apiID)
    else:
        for cat in catList:
            if cat["list"] != [] and cat["_id"] == catID:
                for api in cat["list"]:
                    if tag in api["tag"]:
                        apiIDList.append(api["_id"])
                    elif tag == None:
                        apiIDList.append(api["_id"])
                    else:
                        continue
    return set(apiIDList)


def getAPIInfo(apiID):
    '''
    获取接口详情
    '''
    api_info = {}
    apiDetail = session.get("http://183.131.202.93:9071/api/interface/get?id=" + str(apiID))
    api_data = apiDetail.json()["data"]
    # 获取请求参数列表  json
    args = []
    try:
        if api_data["req_body_type"] == "json":
            try:
                fields = json.loads(api_data["req_body_other"])["properties"]
            except:
                fields = []
            for field in fields:
                args.append(field)
        elif api_data["req_body_type"] == "form":
            fields = api_data["req_body_form"]
            for field in fields:
                args.append(field["name"])
        else:
            pass
    except KeyError:
        args = []

    if "api" in api_data["path"]:
        url = api_data["path"].split("/api")[1]
    else:
        url = api_data["path"]

    api_info.update({
        "url": url,
        "method": api_data["method"],
        "api_name": url.replace("/", "_")[1:],
        "args": args,
        "comment": api_data["title"]
    })
    return api_info


def getModuleName(projectID):
    res = session.get("http://183.131.202.93:9071/api/project/get?id=" + projectID)
    modules = []
    for i in res.json()["data"]["cat"]:
        modules.append(
            {
                "_id": i["_id"],
                "name": i["name"]
            }
        )
    return modules


print("**************************************************************************************************************")

# 创建自动化接口脚本文件

# !!!!! 如果是前台接口在这里修改import
# 前台 from api.hd_front import Front
# 后台 from api.hd_back import BackManage
script_template = '''import pytest
from api.wuhe_back import WuheBack


class Test_{{ name }}:
    data=[
        ()
    ]

    @pytest.mark.parametrize("{{ args }}", data)
    def test_{{ item["api_name"] }}(self{% for a in item['args']%}, {{ a }}{% endfor %}):
        user = Front()
        res = user.{{ item["api_name"] }}({{args}})
        res_json = res.json
        assert res.status_code == 200, "接口级别校验_【{{ item['comment'] }}】 " + "请求链接为：" + res.request.url
        assert res.elapsed.seconds <= 3, "接口响应超时"
        assert res_json['code'] == 0, "code校验_【{{ item['comment'] }}】 " + "请求链接为：" + res.request.url

'''


def save_file(filename, content):
    with open(filename, "w+", encoding="utf-8") as f:
        f.write(content)


import os
import xpinyin

count = 0  # 统计创建的接口脚本文档数量

dirname = os.path.dirname(__file__) + "/testScript/"
modules = getModuleName(projectID)
for module in modules:

    pinyin = xpinyin.Pinyin()

    # 根据接口文档的模块创建文件夹
    workdir = dirname + "test_" + pinyin.get_pinyin(module["name"], "")
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    # 获取对应模块的全部接口
    actions = []

    for api in getAPIList(projectID, module["_id"]):
        if api == apiID:
            actions.append(getAPIInfo(api))
            break
        elif apiID == None:
            actions.append(getAPIInfo(api))
        else:
            continue

    # 循环模块的所有接口生成对应文件
    for item in actions:
        # print(item["api_name"])
        # 类名首字母大写
        name = []
        for i in item["api_name"].split("_"):
            name.append(i.capitalize())
        # 因为方法中最后一个逗号，所以拼接好再传给模板
        args = item["args"]

        content = Template(script_template).render(item=item, name="".join(name), args=", ".join(args))
        filename = workdir + "/" + "test_" + item["api_name"] + ".py"
        save_file(filename, content)
        count += 1

print("共创建{}个脚本文件".format(count))

# if __name__ == '__main__':
#     # print(getModuleName(projectID))
#     print(getAPIList(projectID))
