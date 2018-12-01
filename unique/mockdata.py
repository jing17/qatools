from faker import Faker
import random
from unique.area import areaList
from enum import Enum


class SEX(Enum):
    ALL = 0
    FEMALE = 1
    MALE = 2


class MockData:
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    def getPhone(self):
        '''
        获取手机号
        :return:
        '''
        phone = self.faker.phone_number()
        return phone

    def getEmailAddr(self):
        '''
        获取邮箱地址
        :return:
        '''
        email = self.faker.email()
        return email

    def getName(self, sex=SEX.ALL.value):
        '''
        获取姓名
        :return:
        '''
        if sex == SEX.ALL.value:
            name = self.faker.name()
        elif sex == SEX.FEMALE.value:
            name = self.faker.name_female()
        elif sex == SEX.MALE.value:
            name = self.faker.name_male()

        return name

    def getIDCard(self):
        '''
        获取身份证
        :return:
        '''
        IDCard = self.faker.ssn()
        return IDCard

    def getFruitGoodsName(self):
        '''
        生成水果商品名称
        :return:
        '''
        prefixList = ['百姓', '盛通', '杭果', '焱果', '银芳', '福门', '佳瑶', '辅料', 'Z', '振飞']
        prefixName = random.choice(prefixList)

        fruitList = ['西瓜', '美人瓜', '甜瓜', '香瓜', '黄河蜜', '哈密瓜', '木瓜', '乳瓜', '草莓', '蓝莓', '黑莓', '桑葚', '覆盆子', '葡萄', '青提',
                     '红提', '水晶葡萄', '马奶子', '蜜橘', '砂糖橘', '金橘', '蜜柑', '甜橙', '脐橙', '西柚', '柚子', '葡萄柚', '柠檬', '文旦', '莱姆',
                     '油桃', '蟠桃', '水蜜桃', '黄桃', '李子', '樱桃', '杏', '梅子', '杨梅', '西梅', '乌梅', '大枣', '沙枣', '海枣', '蜜枣', '橄榄',
                     '荔枝', '龙眼', '桂圆', '槟榔', '苹果', '红富士', '红星', '国光', '秦冠', '黄元帅', '梨', '砂糖梨', '黄金梨', '莱阳梨', '香梨',
                     '雪梨', '香蕉梨', '蛇果', '海棠果', '沙果', '柿子', '山竹', '黑布林', '枇杷', '杨桃', '山楂', '圣女果', '无花果', '白果', '罗汉果',
                     '火龙果', '猕猴桃', '菠萝', '芒果', '栗子', '椰子', '奇异果', '芭乐', '榴莲', '香蕉', '甘蔗', '百合', '莲子', '石榴', '核桃', '拐枣']
        fruitName = random.choice(fruitList)

        return "【{0}】{1}".format(prefixName, fruitName)

    def getAddress_POI(self):
        '''
        获取省市区
        :return:
        '''
        addr = random.choice(areaList)
        province = addr["name"]  # 获取省
        addr_city = random.choice(addr["city"])
        city = addr_city["name"]  # 获取市
        area = random.choice(addr_city["area"])  # 获取区

        detail = self.faker.street_address()
        streetNum = random.randint(1, 999)
        detailAddresss = "{}{}号".format(detail, streetNum)  # 获取详细地址

        longitude = str(self.faker.longitude()).replace("-", "")
        latitude = str(self.faker.latitude()).replace("-", "")

        return {"province": province, "city": city, "area": area, "detailAddresss": detailAddresss,
                "longitude": longitude, "latitude": latitude}

    def getRandomNum(self, begin=1, end=999):
        '''
        获取随机数
        :param begin:
        :param end:
        :return:
        '''
        num = self.faker.random.randint(begin, end)
        return num


if __name__ == '__main__':
    mocker = MockData()
    print(mocker.getName())
    print(mocker.getEmailAddr())
