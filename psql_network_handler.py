import click
import pandas as pd
import psycopg2
import psycopg2.extras
from tabulate import tabulate
from time import sleep, localtime, strftime
import warnings
warnings.filterwarnings('ignore')

networkHealth = """
SELECT
TO_CHAR(((EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp())) || ' second')::interval, 'HH24:MI:SS') AS log_delay,
((EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp()))) AS delay_as_interval
"""

getServerIP = """select inet_server_addr()"""

networkActivity = """
SELECT 
-- datname, 
pid, 
usename, 
application_name, 
round((EXTRACT(epoch FROM (SELECT (NOW() - query_start)))/60)::numeric,2) as duration,
state, 
query
FROM pg_stat_activity
WHERE usename %(flag)s
ORDER BY usename DESC
"""

idle_queries = """
SELECT 
-- datname, 
pid, 
usename, 
application_name, 
round((EXTRACT(epoch FROM (SELECT (NOW() - query_start)))/60)::numeric,2) as duration,
state, 
query
FROM pg_stat_activity
WHERE state = 'idle'
AND usename NOT IN ('rdsadmin')
ORDER BY usename DESC
"""

getquery = """
SELECT query
FROM pg_stat_activity
WHERE pid = %(pid)s
ORDER BY usename DESC
"""

killqueryscript = """
SELECT pg_terminate_backend(%(pid)s)
"""

networkHealthOld = """
SELECT
TO_CHAR(((CASE
  WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0
  ELSE EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp())
END) || ' second')::interval, 'HH24:MI:SS') AS log_delay,
((CASE
  WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0
  ELSE EXTRACT (EPOCH FROM now() -pg_last_xact_replay_timestamp())
END)) AS delay_as_interval"""

@click.command()
@click.option('--listquery', '-l', 'listquery', is_flag=True)
@click.option('--network', '-n', 'network', is_flag=True)
@click.option('--ipaddress', '-i', 'ipaddress', is_flag=True)
@click.option('--query', '-q', 'query', default=None)
@click.option('--killquery', '-k', 'killquery', default=None)
@click.option('--allusers', '-a', 'allusers', is_flag=True)
@click.option('--killqueryme', '-km', 'killqueryme', is_flag=True)
@click.option('--killqueryidle', '-ki', 'killqueryidle', is_flag=True)
@click.option('--killqueryuser', '-ku', 'killqueryuser', default=None)
@click.option('--killqueryall', '-ka', 'killqueryall', is_flag=True)
@click.option('--connection', '-c', 'connection', is_flag=True)
# @click.option('--pid', '-p', 'pid', default=12)


def sqlcheck(listquery, network, ipaddress, query, killquery, allusers, killqueryme, killqueryuser, killqueryall,killqueryidle, connection):

    conn_string = "your_connection_string"

    if ipaddress:
        # print the connection string we will use to connect
        print("Connecting to database\n    ->%s" % (conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here

        # execute our Query

        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("%s" % getServerIP)

        # retrieve the records from the database
        records = cursor.fetchall()
        print(records)
        sleep(1)

    if network:
        # print the connection string we will use to connect
        print("Connecting to database\n    ->%s" % (conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here

        # execute our Query
        print('|Datetime         |', '|Delay_as_interval|')
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

    conn = psycopg2.connect(conn_string)

    if not allusers:
        conditional = "in ('your specific user')"
    else:
        conditional = "IS NOT NULL"

    if listquery:
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.max_colwidth', 150)
        pd.set_option('display.width', 1000)
        pd.set_option('display.expand_frame_repr', False)
        df = pd.read_sql(sql=networkActivity % {'flag': conditional}, con=conn)
        # print(tabulate(df,headers='keys', tablefmt='psql'))
        print(df)
        # df.to_csv('queries.csv')

    if killquery:
        df = pd.read_sql(sql=killqueryscript % {'pid': killquery}, con=conn)
        print(tabulate(df,headers='keys', tablefmt='psql'))

    if killqueryme:
        conditional = "= 'your_user'"
        df = pd.read_sql(sql=networkActivity % {'flag': conditional}, con=conn)
        for i in df.index:
            if df['query'][i].startswith('\nSELECT \n-- datname, \npid, \nusename, \napplication_name,'):
                avoid_query = df['pid'][i]
        list_of_pids = df.pid

        for i in list_of_pids:
            if i == avoid_query:
                continue
            else:
                dfkill = pd.read_sql(sql=killqueryscript % {'pid': i}, con=conn)
                if dfkill.pg_terminate_backend[0]:
                    print(f'{i} successfully terminated')
                else:
                    print(f'{i} unsuccessfully terminated')

    if killqueryuser:
        conditional = "in ('{}')".format(killqueryuser)
        df = pd.read_sql(sql=networkActivity % {'flag': conditional}, con=conn)
        list_of_pids = df.pid

        for i in list_of_pids:

            dfkill = pd.read_sql(sql=killqueryscript % {'pid': i}, con=conn)
            if dfkill.pg_terminate_backend[0]:
                print(f'{i} successfully terminated')
            else:
                print(f'{i} unsuccessfully terminated')

    if killqueryidle:
        conditional = "in ('{}')".format(killqueryuser)
        df = pd.read_sql(sql=idle_queries, con=conn)
        list_of_pids = df.pid

        for i in list_of_pids:

            dfkill = pd.read_sql(sql=killqueryscript % {'pid': i}, con=conn)
            if dfkill.pg_terminate_backend[0]:
                print(f'{i} successfully terminated')
            else:
                print(f'{i} unsuccessfully terminated')

    if killqueryall:
        conditional = "NOT IN ('rdsadmin')"
        df = pd.read_sql(sql=networkActivity % {'flag': conditional}, con=conn)
        list_of_pids = df.pid

        for i in list_of_pids:
            try:
                dfkill = pd.read_sql(sql=killqueryscript % {'pid': i}, con=conn)
                if dfkill.pg_terminate_backend[0]:
                    print(f'{i} successfully terminated')
                else:
                    print(f'{i} unsuccessfully terminated')
            except:
                print(f'unsuccessfully terminated')
                conn = psycopg2.connect(conn_string)
                continue

    if query:
        df = pd.read_sql(sql=getquery % {'pid': query}, con=conn)
        df.to_csv('../query.csv')
        print(df)
    conn.close()
if __name__ == "__main__":
    sqlcheck()
