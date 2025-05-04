from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Función para obtener conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

# Función que se ejecuta al iniciar para crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id SERIAL PRIMARY KEY,
            texto TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Ruta principal: muestra la lista de tareas
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tareas;')
    tareas = cur.fetchall()
    conn.close()
    return render_template('index.html', tareas=tareas)

# Ruta para agregar una nueva tarea
@app.route('/add', methods=['POST'])
def add():
    texto = request.form['texto']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tareas (texto) VALUES (%s);', (texto,))
    conn.commit()
    conn.close()
    return redirect('/')

# Ejecutar la app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
