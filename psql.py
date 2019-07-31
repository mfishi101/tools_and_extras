#!/usr/bin/python3
# Python default
from time import localtime, strftime
from tabulate import tabulate
from datetime import datetime
# Installed Libraries
import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import click
# My Libraries


@click.command()
@click.option('--params', '-pr', 'params', is_flag=True)
@click.option('--excel', '-e', 'excel', is_flag=True)
@click.option('--params2', '-pr2', 'params2', is_flag=True)
@click.option('--arguments', '-arg', 'arguments', default=list_of_data)
@click.option('--p', '-p', is_flag=True)
@click.option('--query', '-q', default=adhoc)
@click.option('--dbnetwork', '-db', default=replicamain)
@click.option('--csv', '-c', is_flag=True)
@click.option('--csvname', '-cn', 'csvname', default='dbdata')
@click.option('--rows', '-r', default=3)
@click.option('--tablefmt', '-t', default='psql')
def psql(query, p, dbnetwork, tablefmt, csv, csvname, params, excel, params2, rows, arguments):
    conn_string = dbnetwork
    starttime = (datetime.utcnow())
    print("Started at %s" % (strftime("%Y-%m-%d %H:%M:%S", localtime())))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    if p:
        preview = ' LIMIT %s;' % rows
    else:
        preview = ';'

    if params2:
        params = arguments
        cursor.execute("%s %s" % (query, preview) % {'arg': params})
    elif params:
        if excel:
            df = pd.read_csv('path to csv')
            listmdx = [df['column name'][i] for i in range(len(df.index))]
            strmdx = str(listmdx).strip('[]')
            params = strmdx
        else:
            params = arguments
        cursor.execute("%s %s" % (query, preview) % params)
    else:
        cursor.execute("%s %s" % (query, preview))

    column_names = [i[0] for i in cursor.description]

    records = cursor.fetchall()

    if csv:
        df = pd.DataFrame(np.array(records), columns=column_names)
        df.to_csv(
            'path to download' % (csvname, (strftime("%Y_%m_%d %H_%M_%S", localtime()))),
            index=False, mode='w', header=True)
        print('Downloaded to csv with filename %s.csv' % csvname)

    else:
        print(tabulate(records, headers=column_names, tablefmt=tablefmt))

    cursor.close()
    conn.close()

    endtime = (datetime.utcnow())
    print("Finished at %s" % (strftime("%Y-%m-%d %H:%M:%S", localtime())))
    totaltime = ((endtime - starttime).total_seconds())
    print('Query finished in %s seconds' % totaltime)


if __name__ == "__main__":
    psql()
