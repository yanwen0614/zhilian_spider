import json
import pickle
import re
import sys

import jieba
import requests
from lxml import etree
from spider import HEADER as header

LOCAL = "工作地点："
SALARY = "职位月薪："
REQUSET_NUM = "招聘人数："


class company(object):
    name = ''
    need_people = 0
    recuitment_city = []
    recuitment_pro = []
    recuitment_row_count = 1
    outlier_recuitment_row_count = []
    size = 0
    get_size_tag = 1

    def __init__(self, name, location, city, need_people, url):
        self.name = name
        self.outlier_recuitment_row_count = [0, 0, 0]
        self.recuitment_city = [location]
        self.recuitment_pro = [city]
        self.size = 10
        self.need_people = need_people

    def write(self, file_hook=sys.stdout):
        print(self.name, self.need_people, self.recuitment_row_count, self.need_people/self.recuitment_row_count, file=file_hook)
        print(self.outlier_recuitment_row_count, self.outlier_recuitment_row_count[0]/self.recuitment_row_count, self.outlier_recuitment_row_count[1]/self.recuitment_row_count, self.outlier_recuitment_row_count[2]/self.recuitment_row_count, file=file_hook)
        print(len(self.recuitment_city), self.recuitment_city, file=file_hook)
        print(len(self.recuitment_pro), self.recuitment_pro, file=file_hook)

    def getsize(self, url):
        try:
            r = requests.get(url, headers=header)
            htmltree = etree.HTML(r.text)
            people_range = htmltree.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[1]/strong/text()')[0]
            sizes = re.findall(r'\d+', people_range)

            sizeint = int(sum(int(size) for size in sizes)/len(sizes))
            self.get_size_tag = 1
           # if sizeint < 500:
           #     print(self.name)
            return sizeint+1
        except:
            return 0



def statis(job):
    companys = {}
    jobdict = {'快递员速递员': (4010400, 247), '房地产': (141000, 0), 'IT业':(160000, 0)}
    city_list = '广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 天津 重庆'.split()
    txtfile_name = u'.\_result\{job}\{job}-{city}.txt'
    i = 0


    for city in city_list:
        with open(txtfile_name.format(city=city, job=job), mode='r', encoding='utf-8') as f:
            while 1:
                jsonstr = f.readline()
                if not jsonstr:
                    break
                line = json.loads(jsonstr)
                i += 1

    print(i)


def outlier(location, company, need_people, salary, city):
    tag = [0, 0]
    # 人数多
    tag[0] = 1 if need_people > 30 else 0
    company_cut_list = jieba.lcut_for_search(company)
    tag[1] = 0 if location in company_cut_list or city in company_cut_list else 1
    if sum(tag) == 2:
        return True
    else:
        return False

def main(job):
    return statis(job)


def getneedpeople(company_num, companys):
    sum_ = 0
    for item_ in list(sorted(companys.items(), key = lambda item: -item[1].need_people))[:company_num]:
        sum_ += item_[1].need_people
    return sum_

if __name__ == '__main__':
    job = 'IT业'
    main(job)

