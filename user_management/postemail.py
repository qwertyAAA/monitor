''' 发邮件的库'''
import smtplib

'''邮件文本'''
from email.mime.text import MIMEText

''' SMTP服务器'''
SMTPServer = "smtp.163.com"

''' 发邮件地址'''
sender = "czx17854292984@163.com"

''' 发送者邮箱的密码'''
passwd = "oneczx1993306"





''' 设置发送的内容'''
message = "hello world welcome new world"

''' 转换为邮件版本'''
msg = MIMEText(message)

''' 标题'''
msg["Subject"] = "oneczx"

'''发送者 '''

msg["From"] = sender



''' 创建SMTP服务器 25端口号'''
mailServer = smtplib.SMTP(SMTPServer,25)
''' 登录邮箱'''
mailServer.login(sender,passwd)
''' 发送邮件 发送者 发送对象  内容转为邮件形式的字符串'''
mailServer.sendmail(sender,["czx17854292984@163.com"],msg.as_string())


''' 退出邮箱'''
mailServer.quit()
