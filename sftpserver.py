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
