from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from pylib.yamlloader import get_env
options=get_env('server.conf').config.mainserver

def send_report(txtreport, htmlreport):
    if options.emails is None:
        return
    print "sending email to", options.emails
    try:
        sender = 'system-test-report@elster.com'
        recipients = options.emails
        subject = ' system-test results'
        message = MIMEMultipart('alternative')
        message['To'] = ', '.join(recipients)
        message['From'] = sender
        message['Subject'] = subject
#        message.preamble = subject
        message.epilogue = ''
        p1 = MIMEText(txtreport, 'plain')
        p2 = MIMEText(htmlreport, 'html')
        message.attach(p1)
        message.attach(p2)
        session = smtplib.SMTP('localhost')
        session.sendmail(sender, recipients, message.as_string())
        session.quit()
    except smtplib.SMTPException, e:
        print "Couldn't send report.  %s" % e