import json
from unique.mockdata import MockData
import os

mocker = MockData()
DATA_PATH = os.path.abspath(".") + "\data\data.json"


class DataType:
    NUM = "num"
    ARRAY = "array"
    PHONE = "phone"
    EMAIL = "email"


# 设置数字唯一值并返回，设置phone 或 email
def setValue(varName, dataType=DataType.NUM, value=1, path=DATA_PATH):
    '''dataType: num、array'''
    with open(path, "r") as f:
        data = json.load(f)
        if varName in data.keys():
            if dataType == "num":
                data[varName] += value
            elif dataType == "array":
                data[varName].append(value)
            else:
                raise NameError("The '{}'dataType is not existed".format(dataType))
        else:
            if dataType == "num":
                data[varName] = 1
            elif dataType == "array":
                data[varName] = [value]
            else:
                raise NameError("The '{}'dataType is not existed".format(dataType))

    with open(path, "w") as write:
        json.dump(data, write, indent=4)

    return data[varName]


# 取数字，or 取phone、email的唯一值
def getValue(varName, dataType=DataType.NUM, path=DATA_PATH):
    '''dataType: num、phone、email'''
    with open(path, "r") as f:
        data = json.load(f)
        if dataType == "num":
            return data[varName]
        elif dataType == "phone":
            try:
                phones = data[varName]
            except KeyError as e:
                phones = []
            phone = mocker.getPhone()
            while phone in phones:
                phone = mocker.getPhone()
            return setValue(varName, "array", phone)
        elif dataType == "email":
            try:
                emails = data[varName]
            except:
                emails = []
            email = mocker.getEmailAddr()
            while email in emails:
                email = mocker.getEmailAddr()
            return setValue(varName, "array", email)
        else:
            raise NameError("The '{}'dataType is not existed".format(dataType))

if __name__ == '__main__':
    setValue("test")