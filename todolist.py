from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inizializza il database
def init_db():
    if not os.path.exists('todo.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        if title:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
