# Importando solo lo necesario (creo que estoy exagerando), 'flash' me sigue dando problemas:
from flask import Flask, render_template, request, url_for,redirect
import sqlite3
# from werkzeug.exceptions import abort  # para mostrar una ventana de '404', no me sirvio

# Función para abrir la conexión:
def get_connection():
    conn = sqlite3.connect('database.db')
    # Acceso a la tabla basado en el nombre de las columnas:
    conn.row_factory = sqlite3.Row
    return conn
# Función para seleccionar un 'post' en especifico:
def get_post(id):
    conn = get_connection()
    post = conn.execute('SELECT * FROM people WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# creamos la base de datos:
import init_db
init_db.first_execute()

app = Flask(__name__)
# app.config['SECRET_KEY'] = '2LJ3j2r32RKBH344hb'

# vamanos a "index.html":
@app.route('/')
def home():
    conn = get_connection()  # Abrimos una conexión
    # Seleccionamos todas las 
    story = conn.execute('SELECT * FROM people').fetchall()
    conn.close()
    return render_template('index.html', posts=story)


# veamos más acerca de ... :
@app.route('/about')
def about():
    return render_template('about.html')


# Veamos una de esas historias:
@app.route('/<int:id>')
def story(id):
    story = get_post(id)
    return render_template('history.html', post=story)


# ¡Podremos añadir historias!:
@app.route('/create', methods=('GET', 'POST'))
def create():
    # verificmos que el método/soicitud sea solo 'POST' y luego extraemos/guardamos los datos:
    try:
        if request.method == 'POST':
            name = request.form['nombre']
            mail = request.form['correo']
            title = request.form['titulo']
            cont = request.form['contenido']
            conn = get_connection()
            conn.execute('INSERT INTO people (name, email, title, content) VALUES (?,?,?,?)',
                        (name, mail, title, cont))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        return render_template('create.html')
    except BaseException as e:
        return render_template('error.html', error=e)


# Editaremos un 'post':
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    story = get_post(id)
    if request.method == 'POST':
        try:
            name = request.form['nombre']
            mail = request.form['correo']
            title = request.form['titulo']
            cont = request.form['contenido']

            conn = get_connection()
            conn.execute('UPDATE people SET name=?, email=?, title=?, content=? WHERE id=?',
                        (name, mail, title, cont, id))
            conn.commit()
            conn.close()
        except BaseException as e:  # por si ocurre algpun error:
            return render_template('error.html', error=e)
        return redirect(url_for('home'))
    return render_template('edit.html', post=story)


# Aquí eliminamos una 'entrada':
@app.route('/<id>/delete')  #, methods=('POST',))
def delete(id):
    try:
        db = sqlite3.connect('database.db')  # story = get_post(id)
        cs = db.cursor()  # conn = get_connection()
        cs.execute('DELETE FROM people WHERE id=?', [id])
        db.commit()
        db.close()
        # return redirect(url_for('home'))
        # flash('"{}" fue eliminado exitosamente'.format(post['title']))
    except BaseException as e:
        return render_template('error.html', error=e)
    return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)
