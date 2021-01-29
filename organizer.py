import json
import requests
import datetime
import smtplib
import telegram_send
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
# with open('./content.json','r') as r:
#     content = json.load(r)


response = requests.get("http://0.0.0.0:5000/random")
content = response.json()
articles = []
for art_d in content['random']:
    # print(list(art_d.values())[0])
    msg = list(art_d.values())[0]
    if "- " in msg:
        msg = msg.split('-')
        msg = "\n ".join(msg)
    articles.append(msg)


tobeemailed = "\n===============================================================\n".join(articles)

def send_mail(send_from, send_to, subject, message, files=[],
              server="smtp.gmail.com", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

date = datetime.datetime.today().strftime('%d-%m-%Y')

# send_mail("naivesumit123@gmail.com",["rsumit123@gmail.com"],date+" Revision Articles",tobeemailed,files = [])
# bot_chatID = "1222108633"
# bot_token = "1670042943:AAGhg366eglFEtMx7J7rRBHdGax07XacS4Q"
# def telegram_bot_sendtext(bot_message):

   
#    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
#    print(send_text)

#    response = requests.get(send_text)

#    return response.json()

# test = telegram_bot_sendtext(tobeemailed)
# print(test)


telegram_send.send(messages=[tobeemailed])












# print(content)

# d={"economy":{"india":[{"28-01-2020":"ECONOMIC RECOVERY RBI \n \
#  continuing with its liquidity infusion programs \n \
# - Real interest rates(Repo rate 4%) remain low despite inflation falling to 4.6%. NEW Monetary Framework : agreement between GOI and RBI to adopt inflation targeting in india \n \
# - Rbi continuing it's liquidity infusion programs including the on tap long term repo operations (TLTRO) , Extended from 5 sectors to 26 notified under the Emergency credit line guarantee scheme (ECLGS 2.0) \n \
# - Also continuing it's operation Twist - the elongation of debt maturity structure through simultaneous buying of long term bonds and selling of short term bonds with OMO of 10000 crore \n \
# - acc to IMFs Fiscal monitor database of country fiscal measures the FS of India is 1.8% of GDP .(brazil 8.3% , russia 2.4% , china 4.6 , SA 5.3) \n \
# - india cannot afford fiscal stimulus at the rates of advanced economies due to the lack of fiscal space . However FM says fiscal deficit fears will not derail gov spending \n"
# },
# ],"world":[]},
# "science and tech" :{"policies":[{"28-01-2020":

# "SCIENCE TECHNOLOGY AND INNOVATION POLICY 2020 \n \
# Indian department of science and tech \
# AIMS \n \
# - develop a people centric technology and innovation system . Double private sectors contribution to the GDE on R&D every 5 yrs .\n \
# - blaming miniscule 0.5% of GDP on R&d (2% goal) on inadequate private sector investment. (long term effect not sustainable for private sector)\n \
# - decentralised institutional mechanism balancing top down and bottom up approach ,focusing on administration and finance management , research governance, data regulatory frameworks and system interconnectedness (provides more autonomy to R&D institutions for financial management)\n \
# - promise to explore international standards in grant management \n \
# - the problem of journal paywalls \n \
# - tackle discrimination based on gender , caste , religion , geography, lang , disability . \n"}

# ],"innovations":[]}}

# with open('./content.json','w') as fp:
#     json.dump(d,fp)