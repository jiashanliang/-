# -*- coding: utf-8 -*-
# import requests
# import json
# url = "https://cars.app.autohome.com.cn/cars_v8.8.5/cars/brands-pm2.json?pluginversion=8.8.5"
# res = requests.get(url).text
# res_json = json.loads(res)
#
# lis = []
# for brandlist in res_json['result']['brandlist']:
#     for list_1 in brandlist['list']:
#         item = {}
#         # print list_1
#         item['name'] = list_1['name']
#         item['id'] = list_1['id']
#         lis.append(item)
#         # print item
# with open('info.json','a') as f:
#     f.write(json.dumps(lis))
# # print res_json

#
# with open("brind_info.json","w") as f:
#     res_1 = json.dumps(res_json)
#     f.write(res_1)
# import json
# r = open('info.json','r')
# for line in r:
#     lines = json.loads(line)
#     for item in lines:
#         print item['id']
# import os
# print os.path.abspath("./")

for i in []:
    if i ==1:
        print "EH系列"
