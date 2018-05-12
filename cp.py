# -*- coding: UTF8 -*-

import time
import datetime

import os


'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


'''获取文件的访问时间'''
def get_FileAccessTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


# path = '/home/odoo/odoo-dev/temp'
path = '/home/hsit/service/fus/node_modules/blueimp-file-upload-node/public/files/'

total = 0
total_size = 0
lst = os.listdir(path)
for i in range(0, len(lst)):
    pa = os.path.join(path, lst[i])
    if os.path.isfile(pa):        
        modify_time = get_FileModifyTime(pa)
        if modify_time < '2018-01-01':
            total = total+1            
            size = get_FileSize(pa)
            total_size += size
            # print u'%d. %s 修改时间: %s \r\n 文件大小: %f MB' % (total, lst[i], get_FileModifyTime(pa), size)
            # os.system('scp -r %s odoo@10.10.10.151:/dev/sda1/'% pa)
            os.system('cp -r %s /移动硬盘/'% pa)
            os.system('rm -rf %s' % pa)
print 'total:%d, total-size:%fMB' % (total, total_size)