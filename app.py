import os
import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    con = sqlite3.connect('test.db')
    con.close()
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        date_time = datetime.datetime.today()
        msg = request.form['msg']
        con = sqlite3.connect('test.db')
        c = con.cursor()
        c.execute("CREATE TABLE message(msg,datetime")
        c.execute("INSERT INTO message VALLUES (?,?)", (msg,date_time))
        con.commit()
        c = con.execute("select * from message")
        for row in c:
            result_0 = row[0]
            result_1 = row[1]
        return render_template('index.html', result_0=result_0, result_1=result_1)

if __name__ == '__main__':
    app.debug = True
    app.run()



