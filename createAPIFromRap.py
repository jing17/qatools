import requests
import os, sys
from pithy import request
from jinja2 import Template
from collections import OrderedDict

# projectId = os.getenv("projectid")
# projectId = sys.argv[1]
projectId = 150
interfaceId = 7627
# print(projectId)
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
result = eval(res.text)
# print(res.cookies.items())


items = []

# 获取module
for module in result["projectData"]["moduleList"]:
    print("**********************************************************************")
    print(module["name"])
    for page in module["pageList"]:
        print(page["name"])
        for action in page["actionList"]:

            # if action["id"] == interfaceId:
            print(action["name"])
            comment = page["name"] + "_" + action["name"]

            print(action["requestUrl"].replace("\\", ""))
            url = action["requestUrl"].replace("\\", "")

            print(action["requestUrl"].replace("\\", "").replace("/", "_")[1:])
            api_name = action["requestUrl"].replace("\\", "").replace("/", "_")[1:]

            if action["requestType"] == "2":
                print("post")
                method = "post"

            else:
                print("get")
                method = "get"
            # 获取参数列表（包括类型、参数、二级参数）
            args = []
            for requestpara in action["requestParameterList"]:
                print(requestpara["identifier"])

                parameter_second = []
                if requestpara["dataType"] == "array<object>":
                    for para in requestpara["parameterList"]:
                        print(para["identifier"])
                        parameter_second.append(para["identifier"])
                args.append({
                    "identifier": requestpara["identifier"],
                    "dataType": requestpara["dataType"],
                    "parameterList": parameter_second
                })

            items.append({
                "url": url,
                "method": method,
                "api_name": api_name,
                "args": args,
                "comment": comment,
            })

print("###########################################################")
# print(items)
print("###########################################################")
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
            {% set count = loop.index - 1 %}
            {{args}}=i[{{count}}]
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

print(Template(template).render(items=items))
print("总共{}个接口".format(len(items)))
