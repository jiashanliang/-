# author: Xanto
# email: xanto@vip.163.com
# datetime: 2018/11/21 19:59
# software: PyCharm + Python3.6.2
# project_name: 数据分析职位分析
import json
import time
from queue import Queue
from bs4 import BeautifulSoup
import requests

jobs_description = []
iplist = []
q = Queue()


def get_ip():
    global iplist
    if q.empty():
        with open('./proxies.txt') as fp:
            iplist = fp.readlines()
        for ip in iplist:
            q.put(ip)
    return q.get().replace('\n', '')


def write_txt(jobs):
    if len(jobs):
        print('准备写入{}条数据'.format(len(jobs)))
        with open('job_description.txt', 'w', encoding='utf-8') as fp:
            for i in range(len(jobs)):
                fp.write(jobs[i] + '\n')
                fp.write('-' * 50)
                print('写入进度:{}/{}'.format(i, len(jobs)))
        print('数据写入完毕')
    else:
        print('无数据可写入')


def parse_job(positionId, ip=None):
    global jobs_description
    url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=',
    }

    try:
        if ip:
            proxies = {
                'http': ip,
                'https': ip,
            }
            text = requests.get(url, headers=header, proxies=proxies, timeout=3).text
        else:
            text = requests.get(url, headers=header, timeout=3).text

        bs_obj = BeautifulSoup(text, 'lxml')
        job_description = (bs_obj.select('.job_bt')[0].get_text())
        jobs_description.append(job_description)
        print('已解析:{}条'.format(len(jobs_description)))
        q.put(ip)

    except Exception as e:
        print('ip:\t{}\t\t\t\t无效,重试:{}'.format(ip,positionId))
        return parse_job(positionId, get_ip())


def get_jobList(ip=None, pagNum=1):
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    data = {
        'first': 'true',
        'pn': pagNum,
        'kd': 'python数据分析',
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    try:
        if ip:
            proxies = {
                'http': ip,
                'https': ip,
            }
            response = requests.post(url, data, headers=header, proxies=proxies, timeout=3)
        else:
            response = requests.post(url, data, headers=header, timeout=3)
        # print(response.headers)
        print(pagNum, response.text)

    except Exception as e:
        print('ip:\t{}\t\t\t\t无效,正在重试第{}页'.format(ip,pagNum))
        return get_jobList(get_ip(), pagNum)
    try:
        # 解析json
        ret_data = json.loads(response.text)
        if ret_data['content']['pageNo'] != pagNum:
            print('全部获取完毕')
            return 1
        job_list = ret_data['content']['positionResult']['result']
        print('第[{}]页,本页共[{}]个职位'.format(pagNum, len(job_list)))
        if len(job_list) > 0:
            for i in range(len(job_list)):
                print('正在解析:[{}]-[{}]'.format(pagNum, i + 1))
                parse_job(job_list[i]['positionId'], get_ip())
            q.put(ip)
    except Exception as e:
        print('ip:\t{}\t\t\t\t解析错误,正在重试第{}页'.format(ip,pagNum))
        return get_jobList(get_ip(), pagNum)


def main():
    global jobs_description
    i = 0
    while True:
        i += 1
        ret = get_jobList(get_ip(), i)
        break
        if ret == 1:
            break

    write_txt(jobs_description)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('结束,耗时{:.4f}s'.format((end-start)))


