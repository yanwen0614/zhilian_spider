import json
import jieba

city_list ='广东 湖北 陕西 四川 辽宁 吉林 江苏 山东 浙江 广西 安徽 河北 山西 内蒙 黑龙江 福建 江西 河南 湖南 海南 贵州 云南 西藏 甘肃 青海 宁夏 新疆 北京 上海 天津 重庆'.split()
txtfile_name = u'.\_result\快递员速递员-{city}.txt'
province = {}

with open(txtfile_name.format(city='广东'), mode='r', encoding='utf-8') as f:

    jsonstr = f.readline()
    line = json.loads(jsonstr)
    rawstr = line["详细信息"]
    seg_list = jieba.lcut(rawstr)
    
    print(seg_list)
