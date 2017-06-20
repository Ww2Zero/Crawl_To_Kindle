# -*-coding:utf-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

Email_Host = "smtp.yeah.net"
Sender = 'wwzero@yeah.net'
Receivers = ['Wwstudio@foxmail.com', 'Ww-haha@foxmail.com']
Email_User = "wwzero@yeah.net"
Email_Pass = ""


class EmailUtils(object):

    def __init__(self):
        '''
        初始化 邮件发送地址 邮件接收地址
        '''
        self.senderAddr = Sender
        self.receiveAddrs = Receivers

    def TextEmail(self, subject, content):
        '''
        文本邮件
        '''
        self.message = MIMEText(self._FmtHtmlContent(content), 'html', 'utf-8')
        self.message['From'] = self._FmtMailAddr(self.senderAddr)
        self.message['to'] = self._FmtMailAddr(self.receiveAddrs[0])
        self.message['subject'] = subject

    def MultipartEmail(self,subject):
        '''
        包含附件的邮件
        '''
        self.message = MIMEMultipart()
        self.message['From'] = self._FmtMailAddr(self.senderAddr)
        self.message['to'] = self._FmtMailAddr(self.receiveAddrs[0])
        self.message['subject'] = subject

    def addText(self,content):
        '''
        添加文本
        '''
        TextPart = MIMEText(_FmtHtmlContent(content),'html','utf-8')
        self.message.attach(TextPart)

    def addFile(self,filepath):
        '''
        添加文件
        '''
        filename = os.path.split(filepath)[1]
        with open(filepath,'r')as h:
            contentfile = h.read()
        #设置txt参数
        FilePart = MIMEText(contentfile,'plain','utf-8')
        #附件设置内容类型，方便起见，设置为二进制流
        FilePart['Content-Type'] = 'application/octet-stream'
        #设置附件头，添加文件名
        FilePart['Content-Disposition'] = 'attachment;filename="{}"'%{filename }
        self.message.attach(FilePart)

    def addImage(self,imagepath):
        '''
        添加图片
        '''
        imagename = os.path.split(imagepath)[1]
        with open(imagepath,'rb')as fp:
            picture = MIMEImage(fp.read())
            picture['Content-Type'] = 'application/octet-stream'
            picture['Content-Disposition'] = 'attachment;filename="{}"'%{imagename}
        self.message.attach(picture)

    def _FmtMailAddr(self, mailAddr):
        '''
        格式化 frommail及tomail
        '''
        return '<%s>' % mailAddr

    def _FmtHtmlContent(self, content):
        '''
         格式化 内容
        '''
        return "<html><body><div>{}</div></body></html>".format(content)

    def Send(self):
        '''
        普通方式发送邮件
        '''
        try:
            smtObj = smtplib.SMTP()
            smtObj.connect(Email_Host, 25)
            smtObj.login(Email_User, Email_Pass)
            smtObj.sendmail(self.senderAddr, self.receiveAddrs,
                            self.message.as_string())
            smtObj.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("Error:无法发送邮件")

    def SendWithSSL(self):
        '''
        采用ssl加密方式发送邮件
        '''
        try:
            smtObj = smtplib.SMTP()
            smtObj.connect(Email_Host, 25)
            smtObj = smtplib.SMTP_SSL(Email_Host)
            smtObj.login(Email_User, Email_Pass)
            smtObj.sendmail(self.senderAddr, self.receiveAddrs,
                            self.message.as_string())
            smtObj.quit()
            print("邮件发送成功")
        except Exception as e:
            print(e)
            print("Error:无法发送邮件")


if __name__ == '__main__':
    send = EmailUtils()
    send.TextEmail("kindle 降价了", "明天又是下雨天，不想上班呀")
    send.Send()
