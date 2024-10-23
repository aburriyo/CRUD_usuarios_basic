from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
    conn.close()

init_db()

# Home route to list users
@app.route('/')
def index():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return render_template('usuarios.html', users=users)

# Create a new user
@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        with sqlite3.connect("users.db") as conn:
            conn.execute("INSERT INTO users (nombre, apellido, email) VALUES (?, ?, ?)", (nombre, apellido, email))
        return redirect(url_for('index'))
    
    return render_template('crear_usuario.html')

# View user details
@app.route('/user/<int:user_id>')
def view_user(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    return render_template('ver_usuario.html', user=user)

# Update user
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        with sqlite3.connect("users.db") as conn:
            conn.execute("UPDATE users SET nombre = ?, apellido = ?, email = ? WHERE id = ?", (nombre, apellido, email, user_id))
        return redirect(url_for('index'))
    
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    return render_template('editar_usuario.html', user=user)

# Delete user
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    with sqlite3.connect("users.db") as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
