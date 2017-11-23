# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:33:17 2016

@author: pawel.cwiek
"""

import os
import sqlite3
from time import strftime
import re
from collections import OrderedDict


def dump_stats(subs):
    '''
    takes in list() to count number of files processed
    '''
    db_path = r"\\global.arup.com\europe\Warsaw\Transfer\PCw\_other\log\6SRS"
    if not os.path.exists(db_path):
        #print('not existing', db_path)
        return None

    db_existed = os.path.exists(os.path.join(db_path,'db.sqlite'))
    conn = sqlite3.connect(os.path.join(db_path,'db.sqlite'))
    c = conn.cursor()

    table_name = 'SixSigmaRS_11_log'

    # 'field_name': 'field_type'
    # valid field_type: INT, REAL, TEXT, BLOB, NULL (can add NOT NULL at the end)
    # wtihout ID PRIMARY KEY
    # valid
    columns = OrderedDict([('date','TEXT'),
                           ('file_count','INTEGER'),
                           ('who','TEXT')])
    if not db_existed:
        # create table
        columns_str = ', '.join(('{} {}'.format(cn, ct) for cn, ct in columns.items()))
        c.execute('CREATE TABLE {tn} (ID INTEGER PRIMARY KEY, {cns})'.format(tn=table_name, cns=columns_str))

    now = strftime('%Y-%m-%d_%H%M%S')

    usr_str = os.path.expanduser('~')
    usr_re = re.search( r'[a-z]*\.[a-z]*', usr_str, re.I|re.M)
    usr_str = usr_re.group()
    
    cols = ','.join(columns.keys())
    execute_str = 'INSERT INTO {tn} ({cns}) values ({qmarks})'.format(tn=table_name, cns=cols, qmarks='?,'*len(columns.keys()))
    execute_str = execute_str[:-2]
    execute_str = execute_str + ')'
    c.execute(execute_str, (now,len(subs),usr_str))
    #c.execute('INSERT INTO SixSigmaRS_11_log (date,file_count,who) values (?,?,?)', (now,len(subs),usr_str))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    dump_stats([r'J:\237000\237423-00 Railway line no. 202'])