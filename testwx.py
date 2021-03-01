# coding:utf-8
import itchat
import re


itchat.login()

# 发送消息 
# itchat.send('hello','filehelper')

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
# print friends
for i in friends:
    name = i["NickName"]
# 获取个性签名
    signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
# 正则匹配过滤掉emoji表情，例如emoji1f3c3等
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    print name.encode('GBK', 'ignore')
    print signature.encode('GBK', 'ignore')
    print '-----------------------------'