import imaplib
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from tqdm import tqdm

class Emailer:

    def __init__(self, subject: str, contents: str, mailinglist: list, bcclist: list, send_from: str, images, data: list, dfatt, attachments: list, wbatt, wb_filename: str, username: str, password: str):
        self.send_from = send_from
        self.mailinglist = mailinglist
        self.bcclist = bcclist
        self.subject = subject
        self.contents = contents
        self.images = images
        self.data = data
        self.dfatt = dfatt
        self.attachments = attachments
        self.wbatt = wbatt
        self.wb_filename = wb_filename
        self.username = username
        self.password = password

    def email_smtp(self):

        msg = MIMEMultipart()
        msg['From'] = self.send_from
        msg['To'] = ', '.join(self.mailinglist)
        if self.bcclist:
            msg['Bcc'] = ', '.join(self.bcclist)
        else:
            self.bcclist = []
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.contents, "html"))

        if self.wbatt:
            for i in self.wbatt:				
                attachedfile = MIMEApplication(i.getvalue())
                attachedfile.add_header(
                    'content-disposition', 'attachment', filename=f'{self.wb_filename}.xlsx' )
                msg.attach(attachedfile)

        if self.images:
            for image in self.images:
                with open(image['path'], 'rb') as f:
                    msg_image = MIMEImage(f.read())
                    msg_image.add_header('Content-ID', '<{0}>'.format(image['id']))
                    msg.attach(msg_image)

        if str(type(self.data)) != "<class 'list'>":
            for filename in self.dfatt:    
                attachment = MIMEApplication(self.dfatt[filename](self.data))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                msg.attach(attachment)


        for f in self.attachments:
            with open(f, "rb") as fil: 
                ext = f.split('.')[-1:]
                attachedfile = MIMEApplication(fil.read(), _subtype = ext)
                attachedfile.add_header(
                    'content-disposition', 'attachment', filename=basename(f) )
            msg.attach(attachedfile)


        smtp = smtplib.SMTP(host="TBD") 
        smtp.sendmail(self.send_from, self.mailinglist  + self.bcclist, msg.as_string())
        smtp.close()

    def email_plain(self):

        msg = MIMEMultipart()
        msg['From'] = self.send_from
        msg['To'] = ', '.join(self.mailinglist)
        if self.bcclist:
            msg['Bcc'] = ', '.join(self.bcclist)
        else:
            self.bcclist = []
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.contents, "html"))

        if str(type(self.data)) != "<class 'list'>":
            for filename in self.dfatt:    
                attachment = MIMEApplication(self.dfatt[filename](self.data))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                msg.attach(attachment)


        for f in self.attachments or []:
            with open(f, "rb") as fil: 
                ext = f.split('.')[-1:]
                attachedfile = MIMEApplication(fil.read(), _subtype = ext)
                attachedfile.add_header(
                    'content-disposition', 'attachment', filename=basename(f) )
            msg.attach(attachedfile)


        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465) 
        smtp.ehlo()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.send_from, self.mailinglist  + self.bcclist, msg.as_string())
        smtp.close()

    def delete_email():
		

        my_email = 'your_email@gmail.com'
        app_generated_password = 'custom_app_password'

        #initialize IMAP object for Gmail
        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        #login to gmail with credentials
        imap.login(my_email, app_generated_password)

        imap.select("INBOX")

        status, message_id_list = imap.search(None, 'FROM "email_address@emails.com"')

        #convert the string ids to list of email ids
        messages = message_id_list[0].split(b' ')

        print("Deleting mails")
        for mail in tqdm(messages):
            # mark the mail as deleted
            imap.store(mail, "+FLAGS", "\\Deleted")

        # delete all the selected messages 
        imap.expunge()
        # close the mailbox
        imap.close()
        # logout from the account
        imap.logout()