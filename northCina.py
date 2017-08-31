import pickle

companyspick = open(u'.\_statis\{job}\companys'.format(job ='IT业'), 'rb' )
companys = pickle.load(companyspick)

sortedbynum = sorted(companys.items(), key=lambda item: -sum(item[1].values()))

for c in sortedbynum[:100]:
    cn, citylist, tt = c[0], c[1],sum(c[1].values())
    print(cn, tt)

companyspick.close()
