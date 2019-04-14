"""

Program to manually log data from City Heat usage,
calculate average use per day between logdates
and show in graph
Log_data = Datum
Heat is usage GJ
Flow is usage in m3
Flask Web frontend 
"""




import matplotlib
matplotlib.use('Agg')
from flask import Flask,render_template,request,redirect,url_for
import backend
app = Flask(__name__)

@app.route("/", methods =['GET','POST'])
def home():
    return render_template('entry.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/entry", methods =['GET','POST'])
def entry():
    return render_template('entry.html')

# Add the entry in the database
@app.route("/add", methods=["POST"])
def add():
    print("add")
    addentry = backend.insert(request.form['Log_date'],request.form['Heat'],request.form['Flow'],request.form['Toelichting'])
    # Show the entries from database
    backend.averagecalculation()
    return redirect(url_for('view'))

@app.route("/view" , methods=['GET', 'POST'])
def view():
    # for rows in backend.view():
    #     print (rows)
    rows = backend.view()
    backend.graph_data()
    return render_template('view.html', data=rows)




if __name__ == '__main__':
    app.run(host='192.168.2.252', port=5000)
