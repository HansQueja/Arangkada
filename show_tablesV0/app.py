from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_tables():
    conn = sqlite3.connect('transportV1.db') #establish connection to the db
    cur = conn.cursor() #establish a cursor to execute sql statements/queries
    cur.execute("SELECT * FROM vehicles")
    vehicles = cur.fetchall()
    cur.execute("SELECT * FROM components")
    components = cur.fetchall()
    cur.execute("SELECT * FROM operators")
    operators = cur.fetchall()
    cur.execute("SELECT * FROM routes")
    routes = cur.fetchall()
    conn.close()
    return vehicles, components, operators, routes

@app.route('/')
def index():
    vehicles, components, operators, routes = get_tables()
    return render_template('index.html', vehicles=vehicles, components=components, operators=operators, routes=routes)

if __name__ == "__main__":
    app.run(debug=True)
    