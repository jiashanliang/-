import  pymysql
import requests
import  json

# 接口 ： https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
from sqlalchemy.dialects.mssql import pymssql


def Initialization(page):
    post_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Cookie': 'user_trace_token=20181119134553-1c044f99-c44b-4fb1-863e-577c95179dfe; _ga=GA1.2.1518018158.1542606354; LGUID=20181119134554-615f1f4f-ebbe-11e8-a6d6-525400f775ce; JSESSIONID=ABAAABAAAIAACBIDF692B19D2CE9DE2302DFF38BC87F777; LGSID=20181122163512-87146e49-ee31-11e8-8acd-5254005c3644; PRE_UTM=; PRE_HOST=www.google.co.jp; PRE_SITE=https%3A%2F%2Fwww.google.co.jp%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _gid=GA1.2.1375902786.1542875712; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542606354,1542875712; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; X_HTTP_TOKEN=98574f905ef789092abfe5b08a62982b; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221673a940551be-013d55fa0d77e3-b79183d-1327104-1673a940554134%22%2C%22%24device_id%22%3A%221673a940551be-013d55fa0d77e3-b79183d-1327104-1673a940554134%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542876806; LGRID=20181122165444-41cc214d-ee34-11e8-b44a-525400f775ce; SEARCH_ID=e3e669861bc2409f9b3bc9f068c806ca',
        'Referer': 'https://www.lagou.com/jobs/list_python',
    }
    data = {
        'first': 'true',
        'pn': page,
        'kd': 'python',
    }
    r =requests.post(post_url,headers = headers,data=data)
    return r

def sava_content(response):
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='xzf',
        charset='utf8'
    )
    cursor = connect.cursor()
    response = json.loads(response.text)

    print(type(response))
    works =  response["content"]["positionResult"]["result"]
    for i in range(len(works)):
        work = works[i]
        company = work["companyFullName"]
        position = work["positionName"]
        wages = work["salary"]
        city = work["city"]
        financeStage = work["financeStage"]
        print(company, position, wages, city, financeStage)
        sql = "INSERT INTO lgdata(company,position,wages,city,financeStage) VALUES('%s','%s','%s','%s','%s')" % \
              (company, position, wages, city, financeStage)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            connect.commit()
        except:
            # 发生错误时回滚
            connect.rollback()


if __name__ == '__main__':

    for page in range(1,6):
        response = Initialization(page)
        sava_content(response)
        # down_load(content)