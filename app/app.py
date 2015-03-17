import os
import MySQLdb

from flask import Flask
from flask import request, redirect, render_template, url_for
from flask import Response

app = Flask(__name__)

IP_ADDRESS = os.environ['CLOUDSQL_IP']
PASSWORD = os.environ['CLOUDSQL_PWD'] # or os.environ.get('')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    db=MySQLdb.connect(host=IP_ADDRESS, port=3306, db='guestbook', user='root', passwd=PASSWORD)
    cursor = db.cursor()
    print request.form['entry']
    if request.method == 'POST':
        cursor.execute('INSERT INTO entries (entry) VALUES( ? )', [request.form['entry'],])
        db.commit()
        db.close()
        return redirect(url_for('main_page'))
    else:
        cursor.execute('SELECT * FROM entries')
        entries = [dict(entry=row[0]) for row in cursor.fetchall()]
        db.close()
        return render_template('main.html', entries=entries)

#@app.route('/clear', methods=['POST'])
#def clear_entries():
#    ..
#    return redirect(url_for('main_page'))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
