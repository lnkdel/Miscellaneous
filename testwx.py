# coding:utf-8
import itchat
import re


itchat.login()

# ������Ϣ 
# itchat.send('hello','filehelper')

# ��ȡ�����б�
friends = itchat.get_friends(update=True)[0:]
# print friends
for i in friends:
    name = i["NickName"]
# ��ȡ����ǩ��
    signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
# ����ƥ����˵�emoji���飬����emoji1f3c3��
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    print name.encode('GBK', 'ignore')
    print signature.encode('GBK', 'ignore')
    print '-----------------------------'