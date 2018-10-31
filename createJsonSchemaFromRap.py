import requests
from jinja2 import Template, Environment

# projectId = os.getenv("projectid")
# projectId = sys.argv[1]
projectId = 150
interfaceId = ""

session = requests.session()
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "account": "wujingjing",
    "password": "Jing1991"
}
session.post(url="http://172.16.2.71:8068/account/doLogin.do", data=data, headers=header)

data = {
    "projectId": projectId
}
res = session.post(url="http://172.16.2.71:8068/workspace/loadWorkspace.do", data=data, headers=header)
# print(eval(res.text))
a = type(res.text)
result = eval(res.text)


# print(res.cookies.items())


# 获取返回参数列表并根据id排序，使用递归
def get_respone_para(parameterList):
    paraList = []
    for para in sorted(parameterList, key=lambda x: x["id"]):
        # 参数列表不为空时
        if para["parameterList"] != []:
            paraList.append({
                "identifier": para["identifier"],
                "dataType": para["dataType"],
                "parameterList": get_respone_para(para["parameterList"])
            })

        else:
            paraList.append({
                "identifier": para["identifier"],
                "dataType": para["dataType"],
                "parameterList": []
            })
    return paraList


# 获取接口对应所有字段值，组装成字典
def getInerface(pagename, action):
    comment = pagename + "_" + action["name"]
    url = action["requestUrl"].replace("\\", "")
    api_name = action["requestUrl"].replace("\\", "").replace("/", "_")[1:]

    if action["requestType"] == "2":
        method = "post"
    else:
        method = "get"
    # 获取参数列表（包括类型、参数、二级参数）
    args = get_respone_para(action["responseParameterList"])

    item = {
        # "url": url,
        # "method": method,
        "api_name": api_name,
        "args": args,
        # "comment": comment,
    }
    return item


import json


# 使用json保存的话，可以校验json格式是否正确
def save_file(filename, content):
    with open(filename, "w+", encoding="utf-8") as f:
        json.dump(json.loads(content), f, indent=2)


# def splitString(str):
#     return str.split("|")[0]
#
# env = Environment()
# env.filters.update({
#     'splitString': splitString
# })

template = '''
{
  "type": "object",
  "required": [],
  "properties": {
  {% for item in items %}
    "{{ item['identifier'] }}": {
        "type": "{{item['dataType']}}"{% if item['parameterList'] != [] %},
        "required": [],
        "properties": {
            {% for item in item['parameterList'] recursive %}
                "{{ item['identifier'] }}": {
                    "type": {% if item['parameterList'] == [] %}"{{item['dataType']}}"{% else %}"array",
                    "items": {
                        "type": "object"{% if item['parameterList'] != [] %},
                        "required": [],
                        "properties": {
                            {{ loop(item['parameterList']) }}
                        {% endif %}
                        }
                    }
                    {% endif %}
                }{% if not loop.last %},{% endif %}
            {% endfor %}
            }
        {% endif %}
        }{% if not loop.last %},{% endif %}
  {% endfor -%}
    }
}
'''

# 获取全部module的接口
items = []
for module in result["projectData"]["moduleList"]:
    # print("**********************************************************************")
    for page in module["pageList"]:
        for action in page["actionList"]:
            if action["id"] == interfaceId:
                # items = getInerface(action)
                items.append(getInerface(page["name"], action))
                break
            elif interfaceId == "":
                # items = getInerface(action)
                items.append(getInerface(page["name"], action))
            else:
                continue

# 生成jsonschema文件
import os

count = 0
for item in items:
    print(item["args"])
    content = Template(template).render(items=item["args"])
    print(content)
    filename = os.path.dirname(__file__) + "/jsonSchema/" + item["api_name"] + ".json"
    save_file(filename, content)
    count += 1

# print("###########################################################")
# print(items)
# print("###########################################################")

print("总共创建{}个jsonSchema文件".format(len(items)))

if __name__ == '__main__':
    aa = [{"identifier": 'salePrice',
           "id": 2,
           "dataType": "object",
           "parameterList": [
               {
                   "identifier": "test4444",
                   "id": 4,
                   "dataType": "object",
                   "parameterList": [{
                       "identifier": "test",
                       "id": 3,
                       "dataType": "string",
                       "parameterList": []}]
               },
               {
                   "identifier": "test33333",
                   "id": 3,
                   "dataType": "object",
                   "parameterList": [{
                       "identifier": "test",
                       "id": 5,
                       "dataType": "string",
                       "parameterList": []}]
               }]},
          {"identifier": "test11111111",
           "id": 1,
           "dataType": "string",
           "parameterList": []}
          ]

    print(get_respone_para(aa))
