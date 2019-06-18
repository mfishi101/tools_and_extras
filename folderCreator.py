# default python library
import os

# requires pip installation
import fire

# parameters:
directoryOut = 'C:\\users\\matthew.fisher\\Desktop\\' #full path directory excluding filename with double \ 

createFolder = 'DemoFolder' #create the output folder name

# Creating content. this can seperated into another file and imported via call --> from filename import * <-- do not include extension in the filename.
demoContent1 = """<<html>
<head>
	<meta charset="UTF-8">
	<title>Document</title>
</head>
<body>
	
</body>
</html>
"""

# create functions:

def mkfolder(folderName):
	os.chdir(directoryOut)
	os.makedirs(folderName)

def makefile(fileName='demo', ext='.html', content='demo content'):
	"""
	all content to placed in ''
	default arguments can changed or removed. 
	"""
	os.chdir(directoryOut+createFolder)
	with open(fileName+ext, 'w') as a:
		a.write(content)
		a.close()
		print('completed %s'%fileName)


def runAll():
	mkfolder(createFolder)

	makefile(content=demoContent1)

if __name__ == '__main__':
	fire.Fire(runAll)