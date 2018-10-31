import requests
from jinja2 import Template

# projectId = os.getenv("projectid")
# projectId = sys.argv[1]
projectId = 159
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

# 获取接口对应所有字段值，组装成字典
def getInerface(name, action):
    comment = name + "_" + action["name"]
    url = action["requestUrl"].replace("\\", "")
    api_name = action["requestUrl"].replace("\\", "").replace("/", "_")[1:]

    if action["requestType"] == "2":
        method = "post"
    else:
        method = "get"
    # 获取参数列表（包括类型、参数、二级参数）
    args = []
    for requestpara in sorted(action["requestParameterList"], key=lambda x: x['id']):
        # print(requestpara["identifier"])

        # 二级参数列表
        parameter_second = []
        if requestpara["dataType"] == "array<object>":
            for para in sorted(requestpara["parameterList"], key=lambda x: x['id']):
                parameter_second.append(para["identifier"])
        args.append({
            "identifier": requestpara["identifier"],
            "dataType": requestpara["dataType"],
            "parameterList": parameter_second
        })

    item = {
        "url": url,
        "method": method,
        "api_name": api_name,
        "args": args,
        "comment": comment,
    }
    return item


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

# print("###########################################################")
# # print(items)
# print("###########################################################")
# print(items[0])
# for item in items:
#     print(item["url"], item['method'])
#     break


template = '''
{% for item in items %}
@request(url='{{item['url']}}', method='{{item['method']}}')
def {{item['api_name']}}(self{% for a in item['args']%}, {{a['identifier']}}{% endfor %}):
    """{{item['comment']}}"""
    {% for args in item['args'] -%}{% if args['dataType'] == 'array<object>' -%}{{args['identifier']}}_list = []
    if {{args['identifier']}}:
        for i in {{args['identifier']}}:
        {% for args in args['parameterList'] -%}
            {% set count = loop.index0 %}
            {{args}} = i[{{count}}]
        {% endfor -%}
            {{args['identifier']}}_list.append({
                {% for para in args['parameterList'] -%}
                '{{para}}': {{para}},
                {% endfor -%}
            })
    {% endif -%}
    {% endfor -%}
    json = {
        {% for args in item['args'] -%}
        "{{args['identifier']}}": {% if args['dataType'] != 'array<object>' %}{{ args['identifier'] }},{% else %} {{ args['identifier'] }}_list,{% endif %}
        {% endfor -%}
        }
    return {'json': json, 'headers': self.headers}
{% endfor -%}
'''

# 创建api文档
print(Template(template).render(items=items))
print("总共{}个接口".format(len(items)))

print("**************************************************************************************************************")

# 创建自动化接口脚本文件

script_template = '''import pytest

class Test_{{ name }}:
    data=[
        ()
    ]

    @pytest.mark.parametrize("{{ args }}", data)
    def test_{{ item["api_name"] }}(self{% for a in item['args']%}, {{ a['identifier'] }}{% endfor %}):
        user = Mange(username,pwd)
        res = user.{{ item["api_name"] }}({{args}})
        res_json = res.json
        assert res.status_code == 200, "接口级别校验_【{{ item['comment'] }}】"
        assert res_json['resultCode'] == "0","resultCode校验_【{{ item['comment'] }}】"
'''


def save_file(filename, content):
    with open(filename, "w+", encoding="utf-8") as f:
        f.write(content)


import os
import xpinyin

count = 0  # 统计创建的接口脚本文档数量

dirname = os.path.dirname(__file__) + "/test/"
for module in result["projectData"]["moduleList"]:
    for page in module["pageList"]:

        pinyin = xpinyin.Pinyin()

        # 根据接口文档的模块创建文件夹
        workdir = dirname + "test_" + pinyin.get_pinyin(page["name"], "")
        if not os.path.exists(workdir):
            os.makedirs(workdir)

        # 获取对应模块的全部接口
        actions = []
        for action in page["actionList"]:
            if action["id"] == interfaceId:
                actions.append(getInerface(page["name"], action))
                break
            elif interfaceId == "":
                actions.append(getInerface(page["name"], action))
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
            args = []
            for j in item["args"]:
                args.append(j["identifier"])

            content = Template(script_template).render(item=item, name="".join(name), args=", ".join(args))
            filename = workdir + "/" + "test_" + item["api_name"] + ".py"
            save_file(filename, content)
            count += 1

print("共创建{}个脚本文件".format(count))

if __name__ == '__main__':
    save_file("001", "fsffsf12121")
