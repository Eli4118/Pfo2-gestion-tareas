# app.py
import sqlite3
from flask import Flask, request, jsonify, redirect, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para sesiones
DATABASE = 'tareas.db'

# Función para conectar a la base de datos
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Crear tablas si no existen
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        
        # Crear tabla de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                completada BOOLEAN DEFAULT 0,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        db.commit()

# Cerrar conexión a la base de datos al finalizar
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Endpoint: POST /registro
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    
    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Hash de la contraseña antes de almacenar
        contraseña_hash = generate_password_hash(contraseña)
        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )
        db.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

# Endpoint: POST /login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user['contraseña'], contraseña):
        session['usuario_id'] = user['id']
        session['usuario'] = user['usuario']
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# Ruta principal - Interfaz web
@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login_page')
    return render_template('index.html', usuario=session['usuario'])

# Página de login
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# Endpoint: GET /tareas (HTML)
@app.route('/tareas')
def listar_tareas():
    if 'usuario_id' not in session:
        return redirect('/login_page')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE usuario_id = ?", (session['usuario_id'],))
    tareas = cursor.fetchall()
    
    return render_template('tareas.html', tareas=tareas, usuario=session['usuario'])

# API: CRUD de tareas
@app.route('/api/tareas', methods=['GET', 'POST'])
@app.route('/api/tareas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gestion_tareas(id=None):
    if 'usuario_id' not in session:
        return jsonify({"error": "No autenticado"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # GET - Listar todas las tareas
    if request.method == 'GET' and id is None:
        cursor.execute("SELECT * FROM tareas WHERE usuario_id = ?", (session['usuario_id'],))
        tareas = [dict(row) for row in cursor.fetchall()]
        return jsonify(tareas)
    
    # GET - Obtener tarea específica
    elif request.method == 'GET':
        cursor.execute("SELECT * FROM tareas WHERE id = ? AND usuario_id = ?", (id, session['usuario_id']))
        tarea = cursor.fetchone()
        if tarea:
            return jsonify(dict(tarea))
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    # POST - Crear nueva tarea
    elif request.method == 'POST':
        data = request.get_json()
        descripcion = data.get('descripcion')
        
        if not descripcion:
            return jsonify({"error": "Falta descripción"}), 400
        
        cursor.execute(
            "INSERT INTO tareas (usuario_id, descripcion) VALUES (?, ?)",
            (session['usuario_id'], descripcion)
        )
        db.commit()
        return jsonify({"mensaje": "Tarea creada", "id": cursor.lastrowid}), 201
    
    # PUT - Actualizar tarea
    elif request.method == 'PUT':
        data = request.get_json()
        descripcion = data.get('descripcion')
        completada = data.get('completada')
        
        # Verificar si la tarea existe y pertenece al usuario
        cursor.execute("SELECT * FROM tareas WHERE id = ? AND usuario_id = ?", (id, session['usuario_id']))
        if not cursor.fetchone():
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Actualizar campos modificados
        updates = []
        params = []
        if descripcion:
            updates.append("descripcion = ?")
            params.append(descripcion)
        if completada is not None:
            updates.append("completada = ?")
            params.append(1 if completada else 0)
        
        if not updates:
            return jsonify({"error": "No hay cambios"}), 400
        
        params.append(id)
        query = f"UPDATE tareas SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        db.commit()
        return jsonify({"mensaje": "Tarea actualizada"})
    
    # DELETE - Eliminar tarea
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM tareas WHERE id = ? AND usuario_id = ?", (id, session['usuario_id']))
        db.commit()
        if cursor.rowcount > 0:
            return jsonify({"mensaje": "Tarea eliminada"})
        return jsonify({"error": "Tarea no encontrada"}), 404

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_page')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
