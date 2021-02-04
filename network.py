# postgreSQL stats
import psycopg2
import psycopg2.extras
from time import strftime, localtime

def network(self, dbnetwork):
	conn_string = # enter connection string to db here
	# print the connection string we will use to connect
	print("Connecting to database\n	->%s" % (conn_string))

	# query to get current lag
	networkHealth = """
	SELECT
	TO_CHAR(((CASE
	  WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0
	  ELSE EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp())
	END) || ' second')::interval, 'HH24:MI:SS') AS log_delay,
	((CASE
	  WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0
	  ELSE EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp())
	END)) AS delay_as_interval"""

	# header for our Query
	print('|Datetime         |', '|Delay_as_interval|')

	# loop the query
	while True:
		conn = psycopg2.connect(conn_string)

		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		cursor.execute("%s" % networkHealth)

		# retrieve the records from the database
		records = cursor.fetchall()
		print(strftime("%Y-%m-%d %H:%M:%S", localtime()), ''.join(str(e) for e in records))
		sleep(1)
		# cntrl c to escape
	cursor.close()
	conn.close()
	