# -*- coding: utf-8 -*-
import scrapy
import json
from autohome_app.items import AutohomeAppItem
import re
from copy import deepcopy
import requests


class KoubeiSpider(scrapy.Spider):
    name = 'koubei'
    allowed_domains = ['autohome.com.cn']
    lis1 = []
    lis = []
    r = open("info.json",'r')
    for line in r:
        lines = json.loads(line)
        for item in lines:
            lis.append("https://cars.app.autohome.com.cn/cars_v8.8.5/cars/seriesprice-pm2-b{}-t16-v8.8.5-c110100.json?pluginversion=8.8.5".format(item["id"]))

    start_urls = lis



    def parse(self, response):
        item = AutohomeAppItem()
        # print response.body
        # print response.url
        res = json.loads(response.body)['result']
        item["brand_id"] = re.match(r'https://cars.app.autohome.com.cn/cars_v8.8.5/cars/seriesprice-pm2-b(\d+?)-t16-v8.8.5-c110100.json\?pluginversion=8.8.5',response.url).group(1)
        item["brand_name"] = res["brandname"]
        for i in res['fctlist']:
            for serieslist in i['serieslist']:
                item["serialName"] = serieslist["name"]
                item["serialId"] = serieslist['id']
                # self.lis1.append("a")
                # print len(self.lis1)
                url = "https://koubei.app.autohome.com.cn/autov8.8.5/alibi/seriesalibiinfos-pm2-ss{}-st0-p1-s20-isstruct1-o0.json".format(item["serialId"])
                item["ResultBad"] = []
                item["ResultGood"] = []
                item["goodContent"] = []
                item["badContent"] = []
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_koubei,
                    meta={'item':deepcopy(item)}
                )

    def parse_koubei(self,response):
        item = deepcopy(response.meta["item"])
        res = json.loads(response.body)["result"]
        item["AverageRating"] = res["average"]
        # print item
        Summary = res["structuredlist"][0]["Summary"] if  len(res["structuredlist"]) > 0 else None
        for result in Summary:
            if result["SentimentKey"] == 3:
                item["ResultGood"].append(result["Combination"])
            if result["SentimentKey"] == 2:
                item["ResultBad"].append(result["Combination"])
        # print item
        item["Koubeiid"] = []
        yield scrapy.Request(
            url="https://koubei.app.autohome.com.cn/autov8.8.5/alibi/seriesalibiinfos-pm2-ss{}-st0-p1-s20-isstruct0-o0.json".format(item["serialId"]),
            callback=self.get_eid,
            meta={"item":deepcopy(item),"page_param":1}
        )


    def get_eid(self,response):
        item = deepcopy(response.meta["item"])
        res = json.loads(response.body)["result"]["list"]
        if len(res) != 0:
            for Koubeiid in res:
                item["Koubeiid"].append(Koubeiid["Koubeiid"])
            page_param = response.meta["page_param"] + 1
            next_url = "https://koubei.app.autohome.com.cn/autov8.8.5/alibi/seriesalibiinfos-pm2-ss{}-st0-p{}-s20-isstruct0-o0.json".format(item["serialId"],page_param),
            print "----------"
            print next_url[0]
            print("hhh")
            yield scrapy.Request(
                url=next_url[0],
                callback=self.get_eid,
                meta={
                    "item":deepcopy(item),
                    "page_param":page_param
                }
            )
        else:
            for eid in item["Koubeiid"]:
                detail_url = "https://koubei.app.autohome.com.cn/autov8.8.5/alibi/NewEvaluationInfo.ashx?eid={}&useCache=1".format(str(eid))
                headers = {
                    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
                }
                content = json.loads(requests.get(detail_url,headers = headers).text)
                item["goodContent"].append(content["result"]["bestScene"]["feeling"])
                item["badContent"].append(content["result"]["worstScene"]["feeling"])
            yield item







