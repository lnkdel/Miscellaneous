# coding:utf-8
import requests
from lxml import html
import os
# 编码问题，可以加下面三行
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Cookie': 'd_c0="AIDA0fXzUwqPTskqzrM5eH6SDcZW8v59PuM=|1470212680"; _za=9ce25915-3a81-4bf7-ab9a-80fe5cf3224f; _zap=0d1a4e65-fdcd-4ace-b652-401719701d17; q_c1=9f83679ce46245b786465970eec76f50|1492657648000|1470212679000; _xsrf=aaa746b240158024bf6d66da491e83e7; r_cap_id="YmQyZjE3NzMxYjVjNGVhMDk1YTk3ZDEyMWZkMmUyMjk=|1493005616|43efb730ff7ad05886a5eaf2a75a6000138570be"; cap_id="ODcwMTAxZWJiNmIwNDA4MzljNTZmZDBjZjdkODA4YmM=|1493005616|311652ef66b611c2a7668c2feddb00a5abd57ac7"; aliyungf_tc=AQAAAKsokR+oHQsA07G13UCZj8gNVUl+; acw_tc=AQAAAKwdg16yIgsA07G13Rd6u4PudXtn; __utma=51854390.576299083.1487835076.1494033800.1494220454.60; __utmb=51854390.0.10.1494220454; __utmc=51854390; __utmz=51854390.1494033800.59.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20140215=1^3=entry_date=20140215=1; z_c0=Mi4wQUFEQWxoc21BQUFBZ01EUjlmTlRDaGNBQUFCaEFsVk5QUUlsV1FBdmtNQnV3Sk5oTF9VYjJFREthQkNVZTlTWmFn|1494220949|e93a8e1f91196a6760acad7658cad70cb380b44b'
}


def get_link_ist(collection_num):
    page = input('page count:')
    result = []
    collection_title = None
    for i in range(1, page+1):
        link = 'https://www.zhihu.com/collection/{}?page={}'.format(collection_num, i)
        response = requests.get(link, headers=headers).content
        sel = html.fromstring(response)
        # 创建文件夹
        if collection_title is None:
            # 收藏夹名字
            collection_title = sel.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()')[0].strip()
            if not os.path.exists(collection_title):
                os.mkdir(collection_title)
        each = sel.xpath('//div[@class="zm-item"]//div[@class="zm-item-answer "]/link')
        for e in each:
            link = 'https://www.zhihu.com' + e.xpath('@href')[0]
            result.append(link)
    return [collection_title, result]
    
    
def get_pic(collection, answer_link):
    response = requests.get(answer_link, headers=headers).content
    sel = html.fromstring(response)
    title = sel.xpath('//h1[@class="QuestionHeader-title"]/text()')[0].strip()
    try:
        # 匿名用户
        author = sel.xpath('//a[@class="UserLink-link"]/text()')[0].strip()
    except:
        author = u'匿名用户'
    # 新建路径
    path = collection + '/' + title + ' - ' + author
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        n = 1
        for i in sel.xpath('//div[@class="RichContent-inner"]//img/@src'):
            # 去除whitedot链接
            if 'whitedot' not in i:
                # print i
                pic = requests.get(i).content
                fname = path + '/' + str(n) + '.jpg'
                with open(fname, 'wb') as p:
                    p.write(pic)
                n += 1
        print u'{} 已完成'.format(title)
    except :
        pass


if __name__ == '__main__':
    collection_num = input('Please in put collection No.:')
    r = get_link_ist(collection_num)
    collection = r[0]
    collection_list = r[1]
    for k in collection_list:
        get_pic(collection, k)