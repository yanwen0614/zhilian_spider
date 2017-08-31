import json
import re
from sys import stdout

import jieba
import numpy

from findoutlier import company as company
from companys_process import *


# import requests

LOCAL = "工作地点："
SALARY = "职位月薪："
REQUSET_NUM = "招聘人数："
COMPANY = "公司"





with open('web2shp.txt', mode='r', encoding='utf-8') as f:
        jsonstr = f.read()
        GeoCode = json.loads(jsonstr)


class career(object):
    edulevellist = ('不限', '中技', '初中', '高中', '中专', '大专', '本科', '硕士', '博士')

    def __init__(self, job):
        if job == 'IT业':
            self.careerlist = ('仿真应用工程师', 'Java开发工程师', '手机软件开发工程师', '其他', '平面设计', '通信技术工程师', '电气设计', '计算机辅助设计师', '软件测试', '系统工程师', '高级软件工程师', '算法工程师', '数据库开发工程师', '软件工程师', '信息技术标准化工程师', 'Android开发工程师', '集成电路IC设计/应用工程师', '游戏设计/开发', '需求工程师', '移动互联网开发', '售前/售后技术支持工程师', '网络工程师', '网站架构设计师', 'WEB前端开发', '嵌入式硬件开发', '软件研发工程师', 'ERP技术/开发应用', '系统集成工程师', '用户界面（UI）设计', '用户体验（UE/UX）设计', '脚本开发工程师', '系统架构设计师', '嵌入式软件开发', '美术编辑/美术设计', '硬件工程师', '系统分析员', '系统管理员', 'C语言开发工程师', 'IOS开发工程师', '语音/视频/图形开发', '互联网软件工程师', '数据库管理员',  '游戏界面设计', '电气工程师', '网页设计/制作/美工', 'PHP开发工程师', '游戏策划')
        else:
            self.careerlist = ('房地产内勤', '房地产销售/置业顾问', '房地产销售经理', '房地产销售主管', '会务专员/助理', '房地产评估', '房地产项目开发报建', '其他', '地产店长/经理', '房地产项目策划经理/主管', '房地产项目配套工程师', '大客户销售经理', '监察人员', '咨询顾问/咨询员', '房地产中介/交易', '房地产项目招投标', '房地产项目管理', '房地产项目策划专员/助理', '销售代表', '房地产资产管理', '建筑工程师', '房地产客服')
        self.edu_people_for_career = numpy.zeros((len(self.careerlist), len(self.edulevellist)), dtype=numpy.int32 )

    def update(self, career, edu, people_num):
        career_idx = self.careerlist.index(career)
        edu_idx = self.edulevellist.index(edu)
        self.edu_people_for_career[career_idx, edu_idx] += people_num

    def Display(self, IOhook=stdout):
        print('  ', *self.edulevellist, 'total', file=IOhook,sep=',')
        for i, career in enumerate(self.careerlist):
            print(career, *self.edu_people_for_career[i, :], sum(self.edu_people_for_career[i,:]),file=IOhook,sep=',')
        print('total', *[sum(self.edu_people_for_career[:, i]) for i in range(len(self.edulevellist))],sum(self.edu_people_for_career) , file=IOhook,sep=',')

    def DisplayRate(self, IOhook=stdout):
        print('  ', *self.edulevellist, 'total', file=IOhook,sep=',')
        totalpeople = sum(sum(self.edu_people_for_career))
        for i, career in enumerate(self.careerlist):
            print(career, *[self.edu_people_for_career[i, j]/sum(self.edu_people_for_career[i, :]) for j in range(len(self.edulevellist))], sum(self.edu_people_for_career[i,:])/totalpeople, file=IOhook, sep=',')
        print('total', *[sum(self.edu_people_for_career[:, i])/totalpeople for i in range(len(self.edulevellist))], 1 , file=IOhook,sep=',')


class statis_basic_area(object):
    def __init__(self, name, request_labour=0, salaryArray=[]):
            self.area_name = name
            self.request_labour = request_labour
            self.undeal_labour = 0 
            self.salaryArray = salaryArray[:]

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
        for item in self.salaryArray:
            if type(item) != int:
                print(item)
                print(self.area_name)
        StatisticsVar = self.GetStatisticsVar()

        if StatisticsVar:
            print(self.area_name, self.request_labour+self.undeal_labour, end=' ', file=file)
            print(StatisticsVar[0], StatisticsVar[1], StatisticsVar[2], StatisticsVar[3], StatisticsVar[4], file=file)


class statis_area(statis_basic_area):
    def __init__(self, name, subareas):
        statis_basic_area.__init__(self, name)
        self.area_name = name
        self.subareas = subareas
        self.request_labour = 0
        for subarea in self.subareas:
            self.request_labour = self.request_labour + subarea.request_labour
            self.undeal_labour = self.undeal_labour+subarea.undeal_labour
            self.salaryArray.extend(subarea.salaryArray)

    def GetSubareaByName(self, name):
        for subarea in self.subareas:
            if subarea.area_name == name:
                return subarea
        return 0


def statis(job):
    province = {}
    companys = {}
    #careerlist = set()
    careerstatis=career(job)
    jobdict = {'快递员速递员': (4010400, 247), '房地产': (141000, 0), 'IT业':(160000, 0)}
 #   city_list = '辽宁 吉林   河北 山西  黑龙江 河南'.split()

    city_list = '广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 天津 重庆'.split()
    txtfile_name = u'.\_result\{job}\{job}-{city}.txt'
    i = [0, 0, 0, 0, 0, 0]  # 1人数太多的舍去 2.工资和过大的舍去 3. 每条过大人数的修正 4 每个超过公司地区阈值的舍去, 5 未修改的条码数 6总有效条数
    for city in city_list:
        with open(txtfile_name.format(city=city,job =job), mode='r', encoding='utf-8') as f:
            areas = {}
            while 1:
                jsonstr = f.readline()
                if not jsonstr:
                    break
                line = json.loads(jsonstr)

                location = line[LOCAL].split('-')[0]
                salarys = re.findall(r'\d+', line[SALARY])
                try:
                    salaryint = int(sum(int(salary) for salary in salarys)/len(salarys))
                except:
                    continue
                try:
                    need_people = int(line[REQUSET_NUM][0:-2])
                except:
                    continue
                i[-1] += 1
                if line["公司"] in del_companyslist:
                    i[0] += 1
                    continue
                else:
                    try:
                        people_threshold = companydict[line["公司"]].threshold
                    except:
                        people_threshold = 10


                if salaryint*need_people > 1000000:
                    i[1] += 1
                    continue
                tag = 0
                while 1:

                    if need_people > 10:
                        need_people = int(need_people/3)
                        tag = 1
                    else:
                        break
                
                if line["公司"] not in companys:
                    companys[line["公司"]] = {}
                company_cut_list = jieba.lcut_for_search(line["公司"])
                if location in company_cut_list or city in company_cut_list:
                    if location in companys[line["公司"]]:
                        if companys[line["公司"]][location] < people_threshold*7:
                            companys[line["公司"]][location] += need_people
                            if tag == 0:
                                i[4] += 1
                            else:
                                i[2] += 1
                        else:
                            i[3] += 1
                            continue
                    else:
                        companys[line["公司"]][location] = need_people
                        if tag == 0:
                            i[4] += 1
                        else:
                            i[2] += 1
                else:
                    if location in companys[line["公司"]]:
                        if companys[line["公司"]][location] < people_threshold*5:
                            companys[line["公司"]][location] += need_people
                            if tag == 0:
                                i[4] += 1
                            else:
                                i[2] += 1
                        else:
                            i[3] += 1
                            continue
                    else:
                        companys[line["公司"]][location] = need_people
                        if tag == 0:
                            i[4] += 1
                        else:
                            i[2] += 1
                try:
                    location = GeoCode[location]
                except:
                    continue

                if location not in areas:
                    areas[location] = statis_basic_area(location)
                #careerlist.add(line["职位类别："])
                try:
                    careerstatis.update(line["职位类别："], line["最低学历："],need_people)
                except:
                    continue
                areas[location].request_labour = need_people + areas[location].request_labour
                areas[location].salaryArray.extend([salaryint for x in range(need_people)])
                if not i[-1]%1000:
                    print(i[-1])
            province[city] = statis_area(city, [x for x in areas.values()])
    print(*i)
    
    China = statis_area('China', [province[city] for city in city_list])
    #print(careerlist)
    return China, careerstatis, companys





if __name__ == '__main__':
    job = 'IT业'
    China, careerstatis, companys= statis(job)
    jobdict = {'快递员速递员': (4010400, 247), '房地产': (141000, 0), 'IT业':(160000, 0)}
    
    with open(u'.\_statis\{job}\StatisticsVar_Country.txt'.format(job =job), mode='w', encoding='utf-8') as f:
        print('地区名', '需要人数','均值', '标准差', '最大值', '最小值','中位数', file=f)
        China.DisplayStatisticsVar(file=f)
   
    with open(u'.\_statis\{job}\StatisticsVar_province.txt'.format(job =job), mode='w', encoding='utf-8') as f:
        print('地区名','需要人数', '均值', '标准差', '最大值', '最小值','中位数', file=f)
        for province in China.subareas:
            province.DisplayStatisticsVar(file=f)

    with open(u'.\_statis\{job}\StatisticsVar_area.txt'.format(job =job), mode='w', encoding='utf-8') as f:
        print('地区名', '需要人数', '均值', '标准差', '最大值', '最小值','中位数', file=f)
        for province in China.subareas:
            #print(province.area_name, file=f)
            for area in province.subareas:
                area.DisplayStatisticsVar(file=f)
    
    with open(u'.\_statis\{job}\careerstatis.txt'.format(job =job), mode='w', encoding='utf-8') as f:
        careerstatis.Display(f)
    with open(u'.\_statis\{job}\careerstatis_rate.txt'.format(job =job), mode='w', encoding='utf-8') as f:
        careerstatis.DisplayRate(f)


    def dumpcompanystopickle(companys = companys, job = job):
        with open(u'.\_statis\{job}\companys'.format(job =job), mode='wb', ) as f:
            pickle.dump(companys, f)

    with open(u'.\_statis\{job}\companys_reach_threshold'.format(job =job), mode='w', ) as f:
        for company, people in companys.items():
            peoplett = sum(people.values())
            if peoplett > companydict[company].threshold and peoplett > 500:
                print(company, peoplett, file=f, )
    
    dumpcompanystopickle()
    print('finish')

#   print(i)
#  print(sorted(company.items(), key = lambda item:item[1]))
