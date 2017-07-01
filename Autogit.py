# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

import os
import time
import sys

from ftplib import FTP

reload(sys)
sys.setdefaultencoding('utf8')

devIP = 'xxx.xxx.xxx.xxx'
devPort = '21'
usr = 'xxxxxx'
pwd = '123456'
url = '\\zzinfo-new\\tzt\\jy\\download\\release'
try:
    ftp = FTP()
except Exception:
    print "FTP无法建立连接"
    sys.exit(0)


def connFtp():
    """
    连接FTP
    :return:None
    """
    try:
        ftp.set_debuglevel(2)
        ftp.connect(devIP, devPort)
        ftp.login(usr, pwd)
    except Exception as e:
        print e
        print "FTP连接失败"
        sys.exit(0)


def quitFtp():
    """
    断开FTP
    :return:None
    """
    ftp.quit()


def getChangeStatus():
    """
    获取变动的状态,有变动返回True,无变动返回False
    :return:True/False
    """
    rst = os.popen('git status -s').read()
    if rst == '':
        return False
    else:
        return True


def getChangeFile():
    """
    获取变动的文件名的绝对路径的列表
    :return:List
    """
    if getChangeStatus():
        os.system('git add .')
        os.system('git commit -m"{}"'.format(time.strftime("%Y%m%d%H%M")))
    cmdrst = os.popen("git diff head head^1 --name-only").read()
    print "{}产生了变动，变动信息如下：".format(time.strftime("%Y%m%d%H%M"))
    print cmdrst
    rst = cmdrst.split('\n')
    rst.remove('')
    rstdir = [os.getcwd() + '/' + x for x in rst]
    return rstdir


def getRelaDir(absDir):
    """
    通过绝对路径的分割来获取相对路径
    :param absDir:List, 绝对路径
    :return:List
    """
    relaDir = []
    for x in absDir:
        dir = x.split('release')[1]
        dirlist = dir.split('/')
        for x in dirlist:
            if x == '':
                dirlist.remove('')
        relaUrl = '/'.join(dirlist)
        relaDir.append(relaUrl)
    return relaDir


def upload(filename):
    """
    上传文件
    :param filename:文件名的绝对路径
    :return:None
    """
    print 'uploading {}'.format(filename)
    try:
        fileHandle = open(filename, 'rb')
        ftp.storbinary('STOR {}'.format(os.path.basename(filename)), fileHandle)
        print '{} upload finished'.format(filename)
    except IOError:
        pass


def fuckDS_Store(dsdir):
    """
    干掉该死的DS_Store
    :param dsdir: List, 绝对路径或者相对路径的集合
    :return:List
    """
    for i, x in enumerate(dsdir):
        if 'DS_Store' in x:
            dsdir.pop(i)
    return dsdir


if __name__ == '__main__':
    if getChangeStatus():
        #connFtp()
        absPATH = fuckDS_Store(getChangeFile())
        relaPATH = fuckDS_Store(getRelaDir(absPATH))
        for x, y in zip(relaPATH, absPATH):
            fileinfo = os.path.split(x)
            file_url = os.path.join(url, os.path.split(x)[0]).replace('/', '\\')
            file_name = os.path.split(x)[1]
            #ftp.cwd(file_url)
            #upload(y)
        #quitFtp()
    else:
        print '暂无变化'