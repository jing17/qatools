from jinja2 import Template
import requests, json

# 指定项目>指定标签>指定接口(支持多个)
projectID = "15"
apiID = ["17", "588"]
tag = None

session = requests.session()
body = {
    "email": "wujingj@zjbdos.com",
    "password": "Jing2018"
}
# 登录
res = session.post("http://183.131.202.93:9071/api/user/login", json=body)


def getAPIList(projectID=projectID, apiID=None, tag=None):
    '''
    获取指定条件下所有接口
    '''
    catList = session.get("http://183.131.202.93:9071/api/interface/list_menu?project_id=" + projectID).json()["data"]
    # print(catList)
    apiIDList = []
    if apiID != None:
        apiIDList.extend(apiID)
    else:
        for cat in catList:
            if cat["list"] != []:
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
    if api_data["req_body_type"] == "json":
        fields = json.loads(api_data["req_body_other"])["properties"]
        for field in fields:
            args.append(field)
    elif api_data["req_body_type"] == "form":
        fields = api_data["req_body_form"]
        for field in fields:
            args.append(field["name"])

    else:
        pass

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


items = []
for id in getAPIList(projectID=projectID, apiID=apiID, tag=tag):
    items.append(getAPIInfo(id))

template = '''
{% for item in items %}
@request(url='{{item['url']}}', method='{{item['method']}}')
def {{item['api_name']}}(self{% for a in item['args']%}, {{a}}{% endfor %}):
    """{{item['comment']}}"""
    json = {
        {% for args in item['args'] -%}
        "{{args}}": {{ args }},
        {% endfor -%}
        }
    return {'json': json, 'headers': self.headers}
{% endfor -%}
'''

# 创建api文档
print(Template(template).render(items=items))
print("总共生成{}个接口".format(len(items)))
