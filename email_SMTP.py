import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def sendMail(emailSettings,emailDict,savelocation,reportType,dept,daterange,saveName):

    password = emailSettings.get('PASSWORD')
    port = emailSettings.get('PORT')
    serverName = emailSettings.get('SERVER')
    fromEmail = emailSettings.get('USERNAME')
    emailAdresses = emailDict.get(dept).split(",")

    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = fromEmail
    msg['To'] = emailDict.get(dept)

    try:
        if reportType == 'Report1':
            msg['Subject'] = "Report1 " from " + daterange

            message = ("Good Morning \n\n"
                       "Please find attached Report 1 Over Speeding report from " +daterange +".\nIf there are any issues, please contact webmaster "
                       "\n\nKind regards "
                       "\nTADA")


            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            #-------------------ATTACHMENT PARAMS SINGLE ATTACHEMENT--------------------------
            filename = saveName
            attachment = open(savelocation, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            

            #-------------------ATTACHMENT PARAMS MULTIPLE ATTACHEMENTS--------------------------
            nameOfFile = ['Att1','Att2','Att3','Att4']
            for tempName in nameOfFile:
                filename = tempName + '_' + str(daterange) +'.pdf'
                attachment = open('C:\\Users\\DELL\\Desktop\\PyTest\\Out\\' + filename, "rb")
                file = str('C:\\Users\\DELL\\Desktop\\PyTest\\Out\\' + filename)

                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(file, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                                % os.path.basename(file))
                msg.attach(part)
            
        server = smtplib.SMTP(serverName, int(port))
        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], emailAdresses, msg.as_string())

        # ADDs EMAIL TO SENT ITEMS IN MAILBOX AS READ
        imap = imaplib.IMAP4_SSL(serverName, 993)
        imap.login(fromEmail, password)
        imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        imap.logout()

        server.quit()



        print("successfully sent email to %s\n" % (msg['To']))

    except:
        print("ERROR: Emailing failed sent email to %s\n" % (msg['To']))
