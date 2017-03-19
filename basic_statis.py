
import json
from sys import stdout
import numpy
import re

# import requests

LOCAL = "工作地点："
SALARY = "职位月薪："
REQUSET_NUM = "招聘人数："


with open('GeoCode.txt', mode='r', encoding='utf-8') as f:
        jsonstr = f.read()
        GeoCode = json.loads(jsonstr)

class statis_basic_area(object):
    def __init__(self, name, request_labour=0, salaryArray=[]):
        self.area_name = name
        self.request_labour = request_labour
        self.undeal_labour = 0 
        self.salaryArray = salaryArray[:]
        self.Geocode = self.GetGeocode()

    def GetGeocode(self):

        return GeoCode[self.area_name]


    def GetStatisticsVar(self):
        if self.salaryArray:
            npArray = numpy.array(self.salaryArray, dtype=numpy.int32)
            mean = npArray.mean()
            std = npArray.std()
            _max = npArray.max()
            _min = npArray.min()
            median = numpy.median(npArray)
            return mean, std, _max, _min, median
        return 0

    def DisplayStatisticsVar(self, file=stdout):
        StatisticsVar = self.GetStatisticsVar()
        if StatisticsVar:
            print(self.area_name, self.Geocode[0], self.Geocode[1], self.request_labour+self.undeal_labour, end=' ', file=file)
            print(StatisticsVar[0], StatisticsVar[1], StatisticsVar[2], StatisticsVar[3], StatisticsVar[4], file=file)


class statis_area(statis_basic_area):
    def __init__(self, name, subareas):
        statis_basic_area.__init__(self, name)
        self.subareas = subareas
        self.request_labour = 0
        for subarea in self.subareas:
            self.request_labour = self.request_labour + subarea.request_labour
            self.undeal_labour = self.undeal_labour+subarea.undeal_labour
            self.salaryArray.extend(subarea.salaryArray)

    def GetSubareaByName(self,name):
        for subarea in self.subareas:
            if subarea.area_name == name:
                return subarea
        return 0



city_list ='广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 广州 深圳 天津 重庆'.split()
txtfile_name = u'.\_result\快递员速递员-{city}.txt'

province = {}
for city in city_list:
    with open(txtfile_name.format(city=city), mode='r', encoding='utf-8') as f:
        areas = {}        
        while 1:
            jsonstr = f.readline()
            if not jsonstr:
                break
            line = json.loads(jsonstr)
            if not line[LOCAL] in areas:
                areas[line[LOCAL]] = statis_basic_area(line[LOCAL])
            need_people = int(line[REQUSET_NUM][0:-2])
            areas[line[LOCAL]].request_labour = need_people + areas[line[LOCAL]].request_labour
            salary = re.findall(r'\d+',line[SALARY])
            if len(salary) == 0:
                areas[line[LOCAL]].request_labour = areas[line[LOCAL]].request_labour - need_people
                areas[line[LOCAL]].undeal_labour = areas[line[LOCAL]].undeal_labour + need_people
                break
            elif len(salary) == 1:
                salary = int(salary[0])
            else:
                salary = int((int(salary[0])+int(salary[1]))/2)
            areas[line[LOCAL]].salaryArray.extend([salary for x in range(need_people)])
        province[city] = statis_area(city, [x for x in areas.values()])

China = statis_area('China', [province[city] for city in city_list ])


if __name__ == '__main__':
    with open('StatisticsVar_Country.txt', mode='w', encoding='utf-8') as f:
        print('地区名', '经度', '纬度', '需要人数','均值', '标准差', '最大值', '最小值','中位数', file=f)
        China.DisplayStatisticsVar(file=f)

    with open('StatisticsVar_province.txt', mode='w', encoding='utf-8') as f:
        print('地区名', '经度', '纬度','需要人数', '均值', '标准差', '最大值', '最小值','中位数', file=f)
        for province in China.subareas:
            province.DisplayStatisticsVar(file=f)

    with open('StatisticsVar_area.txt', mode='w', encoding='utf-8') as f:
        print('地区名', '经度', '纬度','需要人数', '均值', '标准差', '最大值', '最小值','中位数', file=f)
        for province in China.subareas:
            for area in province.subareas:
                area.DisplayStatisticsVar(file=f)
    print('finish')



