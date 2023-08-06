
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
# 发送字符串的邮件
from email.mime.text import MIMEText
# 处理多种形态的邮件主体我们需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
# 处理图片需要 MIMEImage 类
from email.mime.image import MIMEImage

# 设置服务器所需信息
fromaddr = '1136865455@qq.com'  # 邮件发送方邮箱地址
password = 'brxhkuaoosefficj'  # 密码(部分邮箱为授权码)
toaddrs = ['3428192414@qq.com', '137xxxxx@qq.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

# 设置email信息
# ---------------------------发送字符串的邮件-----------------------------
# 邮件内容设置
message = MIMEText('hello,ziqiiii', 'plain', 'utf-8')
# 邮件主题
message['Subject'] = 'ziqiiii test email'
# 发送方信息
message['From'] = fromaddr
# 接受方信息
message['To'] =toaddrs[0]
# ---------------------------------------------------------------------


# 登录并发送邮件
try:
    server = smtplib.SMTP('smtp.qq.com',25)  # 163邮箱服务器地址，端口默认为25
    server.login(fromaddr, password)
    server.sendmail(fromaddr, toaddrs, message.as_string())
    print('success')
    server.quit()

except smtplib.SMTPException as e:
    print('error', e)  # 打印错误
