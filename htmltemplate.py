# playing around with a html template renderer
import pandas as pd


x = []

for i in range(5):
	y = str(i+1)
	x.append('%s <br>'%y)
# z = str(x).strip('[]')

y = " ".join(x)


htmltemp = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<title></title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="description" content="">
		<link rel="stylesheet" type="text/css" media="screen" href="css/normalize.css" />
		<link rel="stylesheet" type="text/css" media="screen" href="css/styles.css" />
		<script src="modernizr.js"></script>
	</head>
	<body>

		<a href="http://127.0.0.1:8000/other/">testing</a>
		%s

	</body>
</html>
""" % y




	

temp = open('helloworld.html', 'w')

temp.write(htmltemp)
temp.close()