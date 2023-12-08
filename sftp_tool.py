import pysftp
import base64
import io
import pandas as pd
import numpy as np
from datetime import date

class Sftpserve:
    """sftp server to upload files and function to change permissions of file"""
    def __init__(self, outputfile=None, inputfile=None, outputfolder=None, mode=None):
        self.outputfile = outputfile
        self.inputfile = inputfile
        self.outputfolder = outputfolder
        self.mode = mode
        
    def sftptransfer(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host="host_name_or_ip", username="user", password="pass", cnopts=cnopts) as sftp:
            with sftp.cd(self.outputfolder):
                sftp.put(self.inputfile)
                sftp.chmod(self.outputfile, self.mode)
                # Closes the connection
        sftp.close()

    def getdirectorycontents(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host="host_name_or_ip", username="user", password="pass", cnopts=cnopts) as sftp:
            with sftp.cd('/opt/netUP/incoming'):
                a = sftp.listdir()
                # Closes the connection
        sftp.close()
        return a

    def downloadfiles(self,filename):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host="host_name_or_ip", username="user", password="pass", cnopts=cnopts) as sftp:
            with sftp.cd('/opt/netUP/incoming'):
                xlsx_io = io.BytesIO()
                media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                sftp.getfo(filename, xlsx_io)
                xlsx_io.seek(0)
                data = base64.b64encode(xlsx_io.read()).decode("utf-8")
                href_data_downloadable = f'data:{media_type};base64,{data}'
                return href_data_downloadable
        sftp.close()
        return

    def retrieve_latest(path = '/data/TAL/WebReports', file_prefix = None, ext = '.csv',skiprows=None):

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host="sftp-supply-chain.takealot.com", username="matthew.fisher", password="limewater66", cnopts=cnopts) as sftp:
            with sftp.cd(path):
                a = sftp.listdir()
                a = list(filter(lambda k: file_prefix in k, a))
                a.sort()
                filename = a[len(a)-1]
                if ext == '.csv':
                    df = pd.read_csv(sftp.open(filename, "r"),skiprows=skiprows)
                else:
                    df = pd.read_excel(sftp.open(filename, "r"),skiprows=skiprows)
                    df['filename'] = filename
                    df = df.replace({np.nan: None})
                    df = df.astype('string')
                    df['transaction_date'] = date.today()
        sftp.close()
        return df