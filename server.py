from flask import Flask, render_template, jsonify, request
import sqlite3
from sqlite3 import Error
app = Flask(__name__)


def create_connection():
    try:
        conn = sqlite3.connect('dfs.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)

    return None

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/gettable/")
def getTable():
    conn = create_connection()
    limit = request.args.get('limit')
    with conn:
        cur = conn.cursor()
        if limit != None:
            cur.execute('SELECT * FROM "beginning inventory"' + limit)
        else:
            cur.execute('SELECT * FROM "beginning inventory"')
        rows = cur.fetchall()
        table = []
        for row in rows:
            table.append(tuple(row))
        names = [description[0] for description in cur.description]
        print(names)
        return jsonify(table=table,
                columnnames=names)

app.run(debug=True, host="0.0.0.0", port=80)
