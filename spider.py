import json
import multiprocessing
import random
#from bs4 import BeautifulStoneSoup
from time import sleep

import requests
from lxml import etree

HEADER = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        }

city_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=4010400&sj={job}&jl={city}&sm=1&isfilter=0&isadv=0&pd=-1&sg=8d72699a3b294a0ca519afcdb5b77b6b"
city_list ='陕西 四川 辽宁,广西 安徽 河北 山西,北京,天津 重庆'.split(',')
city_list = [city.split() for city in city_list]
jobdict = {'快递员速递员': 247}
# 广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 

def getReqests(url,header):
    try:
        r = requests.get(url, headers=header)
    except requests.exceptions.ConnectionError as CE:
        print('Forbidden')
        sleep(random.randrange(5,9)+5*random.random())
        r = getReqests(url,header)
    return r

def get_joblist_url(rawurl, citylist, job):
    for city in citylist:
        yield rawurl.format(city=city, job=job)


def get_JobUrlList_and_NextPageUrl(city, job, url):
    # for url in geturl(city_url, city_list, jobdict['快递员/速递员']):
    r = getReqests(url,HEADER)
    htmltree = etree.HTML(r.text)
    job_url_list = htmltree.xpath('//*[@id="newlist_list_content_table"]/div')
    next_page_url = ''.join(htmltree.xpath('//*[@class="pagesDown-pos"]/a/@href'))
    return job_url_list, next_page_url


def get_job_detail_url(job_url_list):
    for job in job_url_list:
        yield job.xpath('./div/ul/li[1]/div/a/@href')

  #  return job_url_list[0].xpath('./div/ul/li[1]/div/a/@href')


def get_text_from_htmltree(htmltree):
    Context_str = ''
    for items in htmltree[0][1:]:
        text = ''.join(items.xpath('./text()'))
        if items.text == ' SWSStringCutEnd ': 
            break
        if text:
            Context_str = Context_str + text
            if len(items) > 1:
                Context_str = Context_str + get_text_from_subdiv(items)
        else:
            Context_str = Context_str + get_text_from_subdiv(items)
    return Context_str

def get_text_from_subdiv(htmltree):
    Context_str = ''
    for items in htmltree:
        text = ''.join(items.xpath('./text()'))
        if text:
            Context_str = Context_str + text
            if len(items) > 1:
                Context_str = Context_str + get_text_from_subdiv(items)
        else:
            Context_str = Context_str + get_text_from_subdiv(items)
    return Context_str

def get_job_information(job_detail_url):
    r = getReqests(job_detail_url,HEADER) 
    htmltree = etree.HTML(r.text)
    job_informations = htmltree.xpath('/html/body/div[6]/div[1]/ul/li')
    job_detailContexts = htmltree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]') 
    job_detailContexts_str = get_text_from_htmltree(job_detailContexts)
    '''
    if  len(job_detailContexts) ==1:
        job_detailContexts = htmltree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/div')
    job_detailContexts_str = ''
    for job_detailContext in job_detailContexts:
        job_detailContexts_str = job_detailContexts_str + ''.join(job_detailContext.xpath('./text()'))
    '''
    infdict = {}
    for inf in job_informations:
        #infstr = '{0}{1}{2}{3}'.format(inf.xpath('./span/text()')[0], ''.join(inf.xpath('./strong/a/text()')), ''.join(inf.xpath('./strong/text()')),''.join(inf.xpath('./strong/span/text()')))
        #print(infstr)
        infdict[''.join(inf.xpath('./span/text()'))] = '{0}{1}{2}'.format( ''.join(inf.xpath('./strong/a/text()')), ''.join(inf.xpath('./strong/text()')),''.join(inf.xpath('./strong/span/text()')))
    infdict['详细信息'] = job_detailContexts_str
    infdict['url'] = job_detail_url
    infdict['公司'] = htmltree.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()')[0]
    return infdict


def main(job, citylist):
    job_tag = jobdict[job]
    for city in citylist:
        url = city_url.format(city=city, job=job_tag)
        urllist, nextpageurl = get_JobUrlList_and_NextPageUrl(city, job_tag, url)
        print(city)
        i = 1
        while 1:
            detailurllist = get_job_detail_url(urllist)
            for detailurl in detailurllist:
                with open(".\\_result\\{job}-{local}.txt".format(job='快递员速递员', local=city),"a",encoding='utf-8') as f:
                    try:
                        f.write(json.dumps(get_job_information(detailurl[0]), ensure_ascii=False,sort_keys=True,)+'\n') # .encode('GBk','ignore').decode('GBk')
                    except:
                        break
            print(i)
            print(nextpageurl)
            i = i + 1
            try:
                urllist, nextpageurl = get_JobUrlList_and_NextPageUrl(url=nextpageurl, city=city, job=job_tag)
            except:
                break
    print('finish')

def multip(job, citylist):
    p = {}
    for i in range(4):
        p[i] = multiprocessing.Process(target=main,args=(job, citylist[i]))

    for i in range(4):
        p[i].start()

    for i in range(4):
        p[i].join()


def test():
    url = "http://jobs.zhaopin.com/453645082250108.htm"
    url = "http://jobs.zhaopin.com/323903815265467.htm"
    url3 = 'http://jobs.zhaopin.com/260652035250284.htm'
    get_job_information(url3)

if __name__ == '__main__':
    multip('快递员速递员',city_list)
    #test()
