import requests
from lxml import etree
#from bs4 import BeautifulStoneSoup
#import time

HEADER = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        }

city_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=4010400&sj={job}&jl={city}&sm=1&isfilter=0&isadv=0&sg=8d72699a3b294a0ca519afcdb5b77b6b"
city_list ='广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 广州 深圳 天津 重庆'.split()
jobdict = {'快递员/速递员': 247}


def get_joblist_url(rawurl, citylist, job):
    for city in citylist:
        yield rawurl.format(city=city, job=job)


def get_job_detail_url():
    # for url in geturl(city_url, city_list, jobdict['快递员/速递员']):
    url = city_url.format(city='广东', job=247)
    r = requests.get(url, headers=HEADER)
    htmltree = etree.HTML(r.text)
    job_url_list = htmltree.xpath('//*[@id="newlist_list_content_table"]/div')

    for job in job_url_list:
        yield job.xpath('./div/ul/li[1]/div/a/@href')

  #  return job_url_list[0].xpath('./div/ul/li[1]/div/a/@href')
        

def get_job_information(job_detail_url):
    r = requests.get(job_detail_url, headers=HEADER) 
    htmltree = etree.HTML(r.text)
    job_informations = htmltree.xpath('/html/body/div[6]/div[1]/ul/li')
    for inf in job_informations:
        infstr = '{0}{1}{2}{3}'.format(inf.xpath('./span/text()')[0], ''.join(inf.xpath('./strong/a/text()')), ''.join(inf.xpath('./strong/text()')),''.join(inf.xpath('./strong/span/text()')))
           
        print(infstr)


urllist = get_job_detail_url()
for url in urllist:
    get_job_information(url[0])
