import json
#from bs4 import BeautifulStoneSoup
from time import sleep
import traceback
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
city_list ='新疆 北京 上海 广州 深圳 天津 重庆'.split()
jobdict = {'快递员速递员': 247}
# 广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 

def getReqests(url,header):
    try:
        r = requests.get(url, headers=header)
    except requests.exceptions.ConnectionError as CE:
        with open("log.txt", 'a') as f:
            traceback.print_exc(file=f)
            f.flush()
            f.close()
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
        

def get_job_information(job_detail_url):
    r = getReqests(job_detail_url,HEADER) 
 
    htmltree = etree.HTML(r.text)
    job_informations = htmltree.xpath('/html/body/div[6]/div[1]/ul/li')
    infdict = {}
    for inf in job_informations:
        #infstr = '{0}{1}{2}{3}'.format(inf.xpath('./span/text()')[0], ''.join(inf.xpath('./strong/a/text()')), ''.join(inf.xpath('./strong/text()')),''.join(inf.xpath('./strong/span/text()')))
        #print(infstr)
        infdict[''.join(inf.xpath('./span/text()'))] = '{0}{1}{2}'.format( ''.join(inf.xpath('./strong/a/text()')), ''.join(inf.xpath('./strong/text()')),''.join(inf.xpath('./strong/span/text()')))
    return infdict

def main(job):
    job_tag = jobdict[job]
    for city in city_list:
        url = city_url.format(city=city, job=job_tag)
        urllist, nextpageurl = get_JobUrlList_and_NextPageUrl(city, job_tag, url)
        print(city)
        i = 1
        while 1:
            detailurllist = get_job_detail_url(urllist)
            for detailurl in detailurllist:
                with open(".\\_result\\{job}-{local}.txt".format(job='快递员速递员', local=city),"a",encoding='utf-8') as f:
                    try:
                        f.write(json.dumps(get_job_information(detailurl[0]), ensure_ascii=False,)+'\n') # .encode('GBk','ignore').decode('GBk')
                    except:
                        break
            print(i)
            print(nextpageurl)
            i = i + 1
            try:
                urllist, nextpageurl = get_JobUrlList_and_NextPageUrl(url=nextpageurl, city=city, job=job_tag)
            except:
                break
            


if __name__ == '__main__':
    main('快递员速递员')
