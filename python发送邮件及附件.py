from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from email.mime.application import MIMEApplication
import smtplib
from datetime import datetime
from worker.db_connection_api import init_config


class SendMail:

    def __init__(self,receive_email):
        self.email = init_config.email
        self.pwd = init_config.email_pwd
        self.receive_email = receive_email

    def send_content(self,receiver_name="数据迁移者",title="数据迁移导出",content="",file_path=""):

        now = str(datetime.now())[:19]
        content = "FYI ,\n\t%s附件是你提交的导出任务的数据，请注意查收，如有问题请联系管理员！"%now

        msg = MIMEMultipart()
        msg['From'] = self.format_address("<%s>" % self.email)
        msg['To'] = self.format_address("%s<%s>" % (receiver_name,self.receive_email))
        msg['Subject'] = Header(title, 'utf-8').encode()

        zipApart = MIMEApplication(open(file_path, 'rb').read())
        zipFile = file_path.split("/")[-1]
        zipApart.add_header('Content-Disposition', 'attachment', filename=zipFile)

        # 邮件正文是MIMEText:
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        msg.attach(zipApart)
        # 配置服务, 默认端口25
        smtp_server = "smtp.exmail.qq.com"
        server = smtplib.SMTP(smtp_server, 25)
        server.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
        server.starttls()

        server.login(self.email, self.pwd)
        server.sendmail(self.email, [self.receive_email], msg.as_string())
        server.quit()

    def send_error(self,receiver_name="数据迁移者",title="数据迁移导出",content=""):
        now = str(datetime.now())[:19]
        content = "管理员服务挂了！%s" % now

        msg = MIMEMultipart()
        msg['From'] = self.format_address("<%s>" % self.email)
        msg['To'] = self.format_address("%s<%s>" % (receiver_name, self.receive_email))
        msg['Subject'] = Header(title, 'utf-8').encode()

        # 邮件正文是MIMEText:
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        # 配置服务, 默认端口25
        smtp_server = "smtp.exmail.qq.com"
        server = smtplib.SMTP(smtp_server, 25)
        server.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
        server.starttls()

        server.login(self.email, self.pwd)
        server.sendmail(self.email, [self.receive_email], msg.as_string())
        server.quit()

    def format_address(self,s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))


# email = SendMail('xxxxxxxx@xx.cn')
# email = SendMail('xxxxxxxx@xx.cn')
# email.send_content(receiver_name="Double",title="测试",file_path="20200829155855.zip")

