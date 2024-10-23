from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Creación y conexión de base de datos
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

# Ruta principal, donde se muestran los usuarios y también se muestran todos los usuarios existentes (SELECT * FROM users)
@app.route('/')
def index():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return render_template('usuarios.html', users=users)

# Crear un nuevo usuario (función especifica para crear "INSERT INTO)
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

# SELECT principalmente de todo, pero específicamente a un usuario en específico
@app.route('/user/<int:user_id>')
def view_user(user_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    return render_template('ver_usuario.html', user=user)

# Actualizar un registro existente (UPDATE WHERE ID)
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

# Eliminar un usuario existente (DELETE WHERE ID)
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    with sqlite3.connect("users.db") as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
