# -*- coding:utf-8 -*-

"""
智能渠道推送工具包

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""
from purequant.config import config
import requests, json, smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from twilio.rest import Client

def dingtalk(data):
    """
    推送钉钉消息。
    :param data: 要推送的数据内容，字符串格式
    :return:
    """
    #  请求地址
    post_url = config.ding_talk_api
    #  消息头部
    headers = {'Content-Type': 'application/json'}
    # 消息主体
    data = {
        "msgtype": "text",
        "text": {
            "content": data
        }
    }
    # 使用post请求推送消息
    requests.post(post_url, data=json.dumps(data), headers=headers)


def sendmail(data):
    """
    推送邮件信息。
    :param data: 要推送的信息内容，字符串格式
    :return:
    """
    from_addr = config.from_addr
    password = config.password
    to_addr = config.to_addr
    smtp_server = config.smtp_server

    msg = MIMEText(data, 'plain', 'utf-8')
    name, addr = parseaddr('Alert <%s>' % from_addr)
    msg['From'] = formataddr((Header(name, 'utf-8').encode(), addr))
    name, addr = parseaddr('交易者 <%s>' % to_addr)
    msg['To'] = formataddr((Header(name, 'utf-8').encode(), addr))
    msg['Subject'] = Header('交易提醒', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 587)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def twilio(message):
    """
    使用twilio推送信息到短信。
    :param message: 要推送的信息，字符串格式。
    :return:
    """
    accountSID = config.accountSID
    authToken = config.authToken
    myNumber = config.myNumber
    twilio_Number = config.twilio_Number
    twilioCli = Client(accountSID, authToken)
    twilioCli.messages.create(body=message, from_=twilio_Number, to=myNumber)

if __name__ == "__main__":
    dingtalk("【交易】 i love you")