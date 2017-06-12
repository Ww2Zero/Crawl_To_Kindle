# -*-coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText


class SendEmail(object):

    def __init__(self, subject, content,
                 senderAddr='wwzero@yeah.net',
                 receiveAddrs='Wwstudio@foxmail.com'):
        self.senderAddr = senderAddr
        self.receiveAddrs = receiveAddrs
        self.message = MIMEText(self.FmtHtmlContent(content), 'html', 'utf-8')
        self.message['From'] = self.FmtMailAddr(senderAddr)
        self.message['to'] = self.FmtMailAddr(receiveAddrs)
        self.message['subject'] = subject

    def FmtMailAddr(self, mailAddr):  # 格式化 frommail及tomail
        return '<%s>' % mailAddr

    def FmtHtmlContent(self, content):  # 格式化 内容
        return "<html><body><div>{}</div></body></html>".format(content)

    def Send(self):
        try:
            smtObj = smtplib.SMTP("smtp.yeah.net")
            smtObj.login("wwzero@yeah.net", "")
            smtObj.sendmail(self.senderAddr, self.receiveAddrs,
                            self.message.as_string())
            smtObj.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("Error:无法发送邮件")
