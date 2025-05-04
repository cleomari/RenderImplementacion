from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tareas (id SERIAL PRIMARY KEY, texto TEXT);')
    cur.execute('SELECT * FROM tareas;')
    tareas = cur.fetchall()
    conn.close()
    return render_template('index.html', tareas=tareas)

@app.route('/add', methods=['POST'])
def add():
    texto = request.form['texto']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tareas (texto) VALUES (%s);', (texto,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
