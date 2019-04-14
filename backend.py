import matplotlib
matplotlib.use('Agg')
import sqlite3
from datetime import date,datetime,timedelta

# Graph curselection
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

def connect():
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS warmte (id INTEGER PRIMARY KEY, log_date text, heat float, flow float)")
    #cur.execute("CREATE TABLE IF NOT EXISTS warmte (id INTEGER PRIMARY KEY, log_date text, heat real, flow real, toelichting text)")
    cur.execute("CREATE TABLE IF NOT EXISTS warmte (id INTEGER PRIMARY KEY, log_date text, heat real, flow real, toelichting text,heatdayaverage real,flowdayaveray real)")
    conn.commit()
    conn.close()

def insert(log_date,heat,flow,toelichting):
    print(log_date,heat,flow,toelichting)
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO warmte VALUES(NULL,?,?,?,?,0,0)",(log_date,heat,flow,toelichting))
    conn.commit()
    conn.close()
    averagecalculation()

def view():
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM warmte ORDER BY date(log_date) DESC")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(log_date="",heat="",flow="",toelichting=""):
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM warmte WHERE log_date=? OR heat=? OR flow=? or Toelichting=?", (log_date,heat,flow,toelichting))
    rows=cur.fetchall()
    conn.close()
    return rows


def delete(id):
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM warmte WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id,log_date,heat,flow,toelichting):
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    cur.execute("UPDATE warmte SET log_date=?, heat=?, flow=?, toelichting=? WHERE id=?", (log_date,heat,flow,toelichting,id))
    conn.commit()
    conn.close()

# Calculate average use per day and insert values of: Log_date, Calculated_Heat_use_day,Calculated_Flow_use_day
def averagecalculation():
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    cur=conn.cursor()
    # Select rows without a calculated average to use in averages calculation
    cur.execute("SELECT id,log_date,heat,flow,heatdayaverage,flowdayaveray FROM warmte WHERE heatdayaverage=0 ORDER BY date(log_date) DESC LIMIT 2")
    lastentries=cur.fetchall()
    print(lastentries)
    print(len(lastentries))
    # Determine the previousentry to use

    # Only calculate if at least 2 values are available to calculate with
    if len(lastentries) > 1:
        # Calculation only to do if 2 values are 0
        previousid = str(int([i[0] for i in lastentries][1]))
        print(previousid)
        # select the line with the ID of the previously manually entered data
        cur.execute("SELECT id,log_date,heat,flow,heatdayaverage,flowdayaveray FROM warmte WHERE id=?", (previousid,))
        previousentry=cur.fetchall()
        print("lastentry =" + str(lastentries) + " previousentry= "+ str(previousentry))

        # Get the values of the last entered
        lastdate = [i[1] for i in lastentries][0]
        lastheat = [i[2] for i in lastentries][0]
        lastflow = [i[3] for i in lastentries][0]
        print(lastdate, lastheat, lastflow)

        # Get the values of the previous ID
        previousdate = [i[1] for i in lastentries][1]
        previousheat = [i[2] for i in lastentries][1]
        previousflow = [i[3] for i in lastentries][1]
        print(previousdate, previousheat, previousflow)

        # Determine the number of days in between last and previous
        datetime_object_last = datetime.strptime(lastdate, '%Y-%m-%d')
        datetime_object_previous = datetime.strptime(previousdate, '%Y-%m-%d')
        delta = datetime.date(datetime_object_last) - datetime.date(datetime_object_previous)
        print (delta.days)
        #
        # # Calculate averages for heat and flow
        average_heat = (lastheat-previousheat)/(delta.days)
        average_flow = (lastflow-previousflow)/(delta.days)
        print(average_heat,average_flow)
        # # Insert or update averages per day
        # # for every day without a value insert: log_date, 0,0,average_heat,average_flow
        next_date = datetime_object_previous + timedelta(days=1)
        # next_date = datetime_object_previous

        if delta.days != 0:
        #
        # # Update to be added on first date and last date
        # # formatted_date = datetime_object_previous.strftime('%d-%m-%Y')
            cur.execute("UPDATE warmte SET  toelichting=?, heatdayaverage=?, flowdayaveray=? WHERE id=?", ("Calculated average",average_heat,average_flow,previousid))
            conn.commit()
            for x in range(delta.days-1):
                formatted_date = next_date.strftime('%Y-%m-%d')
                print(formatted_date)
                cur.execute("INSERT INTO warmte VALUES(NULL,?,?,?,?,?,?)",(formatted_date,"0","0","Calculated average due to no entry",average_heat,average_flow))
                conn.commit()
                next_date = next_date + timedelta(days=1)
                x += 1
            conn.close()
        else:
            print("Number of days < 1")
        return
    else:
        print("slechts 1 waarde in entries")


def graph_data():
    conn=sqlite3.connect("/var/www/warmte/warmtemeter.db")
    c=conn.cursor()
    c.execute('SELECT log_date, heatdayaverage,flowdayaveray FROM warmte ORDER BY log_date ASC')
    data = c.fetchall()
    conn.close()

    dates = []
    values_heat = []
    values_flow = []
    y=[values_heat,values_flow]
    labels =["heat","flow"]
    colors=['r','g','b']
    for row in data:
         dates.append(parser.parse(row[0]))
         values_heat.append(row[1])
         values_flow.append(row[2])
    print(len(y))
    plt.figure(figsize=(15,4))
    # loop over data, labels and colors
    for y_arr, label in zip(y, labels):
        plt.plot(dates, y_arr, label=label)

    plt.title("Heat and flow per day", loc='center')
    plt.legend()
    plt.savefig('/var/www/warmte/static/images/plot.png',transparent=True)
    # plt.show()





connect()
print (view())
