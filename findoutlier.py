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
    get_size_tag = 0

    def __init__(self, name, location, city, need_people):
        self.name = name
        self.outlier_recuitment_row_count = [0, 0, 0]
        self.recuitment_city = [location]
        self.recuitment_pro = [city]
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
    jobdict = {'快递员速递员': (4010400, 247), '房地产': (141000, 0), 'IT业':(160000, 0)}
    city_list = '广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 天津 重庆'.split()
    txtfile_name = u'.\_result\{job}\{job}-{city}.txt'
    i = 0
    companys = {}
    outlierfile = open(u'.\_result\{job}\{job}-outlier'.format(job=job), 'w', encoding='utf-8')
    for city in city_list:
        with open(txtfile_name.format(city=city, job=job), mode='r', encoding='utf-8') as f:
            print(city)
            print(city, file=outlierfile)
            areas = {} 
            while 1:
                jsonstr = f.readline()
                if not jsonstr:
                    break
                line = json.loads(jsonstr)
                try: 
                    need_people = int(line[REQUSET_NUM][0:-2])
                except:
                    continue
                location = line[LOCAL].split('-')[0]
                salary = re.findall(r'\d+', line[SALARY])
                if len(salary) == 0:
                    continue
                if len(salary) == 1:
                    salaryint = int(salary[0])
                else:
                    salaryint = int((int(salary[0])+int(salary[1]))/2)

                if line["公司"] in companys:
                    companys[line["公司"]].need_people += need_people
                    companys[line["公司"]].recuitment_row_count += 1
                    if location not in companys[line["公司"]].recuitment_city:
                        companys[line["公司"]].recuitment_city.append(location)
                    if city not in companys[line["公司"]].recuitment_pro:
                        companys[line["公司"]].recuitment_pro.append(city)

                else:
                    companys[line["公司"]] = company(line["公司"], location, city, need_people)

                i += 1
                if not i % 10000:
                    print(i)

                tag = [0, 0]
                if salaryint*need_people > 1000000:
                    tag[0] = 1
                    # salaryint = int(salaryint/10)
                if outlier(location, line["公司"], need_people, salaryint, city):
                    tag[1] = 1

                if tag == [1, 0]:
                    print(line['url'], line["公司"], salaryint, need_people,'sum_salary_excpect',file=outlierfile)
                    companys[line["公司"]].outlier_recuitment_row_count[0] += 1
                elif tag == [0, 1]:
                    print(line['url'], line["公司"], salaryint, need_people,'outlier', file=outlierfile)
                    companys[line["公司"]].outlier_recuitment_row_count[1] += 1
                elif tag == [1, 1]:
                    print(line['url'], line["公司"], salaryint, need_people,'sum_salary_excpect', 'outlier', file=outlierfile)
                    companys[line["公司"]].outlier_recuitment_row_count[0] += 1
                    companys[line["公司"]].outlier_recuitment_row_count[1] += 1
                    companys[line["公司"]].outlier_recuitment_row_count[2] += 1

    print(i)
    return companys


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
    print(job)
    companys = main(job)
    with open('.\_result\IT业\IT业-companys_size','r',encoding='utf-8') as f:
        while 1:
            rec = f.readline()
            if not rec:
                break
            rec = rec.split()
            if len(rec) > 2:
                rec = [rec[0], ' '.join(rec[1:])]
            try:
                companys[rec[1]].size = int(rec[0])
            except:
                print(rec[1])
    companyspick = open(u'.\_result\{job}\{job}-companys.pickle'.format(job=job), 'wb')
    pickle.dump(companys, companyspick)





