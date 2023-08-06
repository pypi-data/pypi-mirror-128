#!/usr/bin/python3

import sqlite3
from xls_report import XLSReport

connect = sqlite3.connect("chinook.sqlite")
cursor = connect.cursor()
report = XLSReport({
    'cursor': cursor,
    'xml': 'test_xls.xml',
    # 'callback_url': 'http://localhost',
    # 'callback_token': '12345',
    # 'callback_frequency': 20,
    'parameters': {
        'title0': 'Invoices',
        'customer': '',
        'title1': 'Albums',
        'title2': 'Money',
        'title3': 'Sales',
        'title4': 'Customers',
        'artist': ''}
})
report.to_file('test.xls')
cursor.close()
connect.close()
