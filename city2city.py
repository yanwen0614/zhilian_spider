import json


'''
cityfile = open('citylist.txt', mode='r', encoding='utf-8')
cityfile2 = open('citylist2', mode='r', encoding='utf-8')
cityfile3 = open('citylist3', mode='a', encoding='utf-8')
citydict = {}
citylist = []

for city in cityfile2.readlines():
    citylist.append(city[:-1])


for city in cityfile.readlines():
    i= 0
    city = city[:-1]
    for city_true in citylist:
        if city_true.startswith(city):
            citydict[city] = city_true
            i = 1
            break
    if i == 0:
        cityfile3.write(city+'\n')
        cityfile3.flush()

jsonstr = json.dumps(citydict, ensure_ascii=False, sort_keys=True)

with open('GeoCode2.txt', mode='w', encoding='utf-8') as f:
        f.write(jsonstr)
'''

def check():
    with open('citylist2', mode='r', encoding='utf-8') as f:
        citys = f.readlines()
    with open('GeoCode2.txt', mode='r', encoding='utf-8') as f:
        GeoCode = json.loads(f.read())
    for k in GeoCode.values():
        if k+'\n' not in citys:
            print(k, GeoCode[k])


check()