from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random
from flights import generate_flights

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia por algo más seguro en producción
DB_NAME = 'users.db'


# Función para inicializar la base de datos
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()


# Ruta principal (menú)
@app.route('/')
def index():
    return render_template('index.html')


# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return render_template('register.html', error="El usuario ya existe. Intenta con otro nombre.")
    return render_template('register.html', error=None)


# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('radar'))
            else:
                return render_template('login.html', error="Usuario o contraseña incorrectos.")
    return render_template('login.html', error=None)


# Ruta del radar (requiere inicio de sesión)
@app.route('/radar')
def radar():
    if 'username' not in session:
        return redirect(url_for('login'))
    flights = generate_flights()
    return render_template('radar.html', flights=flights)


# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
