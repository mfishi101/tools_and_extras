import yagmail
import os

currentpath = os.path.dirname(os.path.abspath(__file__))

class Emailer:
  def __init__(self, mailinglist, subject, contents, attachments=None):
    self.mailinglist = mailinglist
    self.subject = subject
    self.contents = contents
    self.attachments = attachments


  def email(self):
  	yag = yagmail.SMTP('email', 'password')
  	yag.send(self.mailinglist, self.subject, self.contents, attachments=self.attachments)

# example layout
# testemail = Emailer(mailinglist=['mfishi101@gmail.com'],
# 	 subject='subject',
# 	 contents=[
# 	    "This is the body, and here is just text",
# 	    "You can find an audio file attached."
# 	], attachments=['%s/assets/hublist.csv' % currentpath, '%s/assets/SLAguide.csv' % currentpath])

# example running the emails
# if __name__ == '__main__':
#   testemail.email()


# using outlook to send mail
def sendmailout(to, subject, body, attachments=False):
	"""
	Use outlook to send email
	"""
	import win32com.client as win32
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = to
	mail.Subject = subject
	mail.Body = 'ph'
	mail.HTMLBody = body  # html format

	if attachments:
		for attach in attachments:
			mail.Attachments.Add(attach)

	mail.Send()