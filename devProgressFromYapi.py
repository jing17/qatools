import requests
import xlwt

# 通过tag配置导出对应版本的接口，None为全部
version = None

session = requests.session()
body = {
    "email": "wujingj@zjbdos.com",
    "password": "Jing2018"
}

# 登录
res = session.post("http://yapi.demo.qunar.com/api/user/login", json=body)
# print(res.json())

# 指定项目所有api
catList = session.get("http://yapi.demo.qunar.com/api/interface/list_menu?project_id=29936").json()["data"]
print(catList)

apiDetail = session.get("http://yapi.demo.qunar.com/api/interface/get?id=272377")
# print(apiDetail.json()["data"]["res_body"])


apis = []
for cat in catList:
    if cat["list"] != []:
        for api in cat["list"]:
            if version in api["tag"]:
                apis.append({
                    "catName": cat["name"],
                    "apiName": api["title"],
                    "apiUrl": api["path"]
                })
            elif version == None:
                apis.append({
                    "catName": cat["name"],
                    "apiName": api["title"],
                    "apiUrl": api["path"]
                })
            else:
                continue


print("***********************************")
print(apis)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("接口列表")

# 表头
sheet.write(0, 0, "序号")
sheet.write(0, 1, "模块")
sheet.write(0, 2, "接口名称")
sheet.write(0, 3, "接口地址")
sheet.write(0, 4, "开发状态")
sheet.write(0, 5, "测试状态")

# 列宽
sheet.col(0).width = 256 * 5
sheet.col(1).width = 256 * 20
sheet.col(2).width = 256 * 25
sheet.col(3).width = 256 * 15
sheet.col(4).width = 256 * 15
sheet.col(5).width = 256 * 15

for i, api in enumerate(apis):
    sheet.write(i + 1, 0, i + 1)
    sheet.write(i + 1, 1, api["catName"])
    sheet.write(i + 1, 2, api["apiName"])
    sheet.write(i + 1, 3, api["apiUrl"])
    sheet.write(i + 1, 4, "未开发")
    sheet.write(i + 1, 5, "未测试")
workbook.save("file/apis.xls")
