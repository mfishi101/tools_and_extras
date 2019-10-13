import pysftp

class Sftpserve:
	"""sftp server to upload files and function to change permissions of file"""
	def __init__(self, outputfile, inputfile, outputfolder='dest_folder_on_server', mode=777):
		self.outputfile = outputfile
		self.inputfile = inputfile
		self.outputfolder = outputfolder
		self.mode = mode
		
	def sftptransfer(self):
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		with pysftp.Connection(host="hostname", username="user", password="password", cnopts=cnopts) as sftp:
			with sftp.cd(self.outputfolder):
				sftp.put(self.inputfile)
				sftp.chmod(self.outputfile, self.mode)
				# Closes the connection
		sftp.close()

# option for ftp (port 21) as well
# can just wrap this in a function like above and make dynamic for calling in multiple areas

from ftplib import FTP 
import os

ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('ftphostname', 21) 
ftp.login('username','password')

localfile = 'path_of_file_to_upload'

fp = open(localfile, 'rb')

ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
fp.close()
ftp.quit()