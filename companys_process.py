import pickle
from findoutlier import company as company

job = 'IT业'
companyspick = open(u'.\_result\{job}\{job}-companys.pickle'.format(job=job), 'rb' )
companydict = pickle.load(companyspick)
companyspick.close()

del_companyslist = [item[1].name for item in companydict.items() if item[1].need_people/item[1].recuitment_row_count > 100]

for company in companydict.values():
    company.threshold = company.size/(10*(5*len(company.recuitment_city)+2))

job = 'IT业'
'''
大连摩比维迪视频系统有限公司 1008
大连中软卓越信息技术有限公司 1005
哈尔滨中软国际信息技术有限公司 1003
大连淘车网络科技有限公司 1002
大连淘车网络科技有限公司沈阳办事处 850
大连摩比维迪视频系统有限公司沈阳办事处 752
上海众阮信息科技有限公司大连分公司 747
郑州速龙信息技术有限公司 621
沈阳东软软件人才培训中心 609
大连中科云信息技术有限公司 596
郑州智游联动教育咨询有限公司 591
郑州讯奥信息技术有限公司 573
郑州智游天下电子科技有限公司 555
河南奥之元电子科技有限公司 554
天津开发区中软卓越信息技术有限公司太原办事处 550
郑州昂那克软件科技有限公司 532
郑州卓研云信息科技有限公司 529
中青才智教育投资(北京)有限公司 473
华锐祥博(北京)科技有限公司 467
北京快乐科技有限公司石家庄办事处 448
大连东软软件人才培训中心 426
沈阳睿源科技有限公司 414
长春中软卓越科技有限公司 414
大连创海致诚科技有限公司 399
郑州光速信息技术有限公司 394
荣新中关村IT人才服务中心 365
北京快乐学网络科技有限公司 352
北京中软国际教育科技有限公司长春分公司 347
大连东软睿道教育信息服务有限公司 330
'''



