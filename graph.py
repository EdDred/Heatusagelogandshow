import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')
import sqlite3
import time
import datetime

def graph_data():
    conn=sqlite3.connect("warmtemeter.db")
    c=conn.cursor()
    c.execute('SELECT log_date, average_heat FROM warmte')
    data = c.fetchall()
    conn.close()

    dates = []
    values = []
    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])
    fig = plt.figure()
    fig.savefig('plot.png')
