from flask import Flask, render_template, request, url_for,redirect
import sqlite3

# ***************************************************************** #

# Función para abrir la conexión:
def get_connection():
    connect = sqlite3.connect('database.db')
    # Acceso a la tabla basado en el nombre de las columnas:
    connect.row_factory = sqlite3.Row
    return connect
# Función para seleccionar un 'post' en especifico:
def get_post(id):
    connect = get_connection()
    post = connect.execute('SELECT * FROM people WHERE id = ?',
                        (id,)).fetchone()
    connect.close()
    if post is None:
        abort(404)
    return post

# Creamos la base de datos:
import init_db
init_db.first_execute()


# ***************************************************************** #


app = Flask(__name__)


# Inicio:
@app.route('/')
def home():
    connect = get_connection()  # Abrimos una conexión
    # Seleccionamos todas las 
    story = connect.execute('SELECT * FROM people').fetchall()
    connect.close()
    return render_template('index.html', posts=story)


# Acerca de:
@app.route('/about')
def about():
    return render_template('about.html')


# Mostrar una historia:
@app.route('/<int:id>')
def story(id):
    story = get_post(id)
    return render_template('story.html', post=story)


# Añadir:
@app.route('/create', methods=('GET', 'POST'))
def create():
    try:
        if request.method == 'POST':
            name = request.form['nombre']
            mail = request.form['correo']
            title = request.form['titulo']
            cont = request.form['contenido']
            connect = get_connection()
            connect.execute('INSERT INTO people (name, email, title, content) VALUES (?,?,?,?)',
                        (name, mail, title, cont))
            connect.commit()
            connect.close()
            return redirect(url_for('home'))
        return render_template('create.html')
    except BaseException as e:
        return render_template('error.html', error=e)


# Editar:
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    story = get_post(id)
    if request.method == 'POST':
        try:
            name = request.form['nombre']
            mail = request.form['correo']
            title = request.form['titulo']
            cont = request.form['contenido']

            connect = get_connection()
            connect.execute('UPDATE people SET name=?, email=?, title=?, content=? WHERE id=?',
                        (name, mail, title, cont, id))
            connect.commit()
            connect.close()
        except BaseException as e:  # por si ocurre algpun error:
            return render_template('error.html', error=e)
        return redirect(url_for('home'))
    return render_template('edit.html', post=story)


# Eliminar:
@app.route('/<id>/delete')  #, methods=('POST',))
def delete(id):
    try:
        connect = get_connection()
        connect.execute(' DELETE FROM people WHERE id=? ', [id])
        connect.commit()
        connect.close()
    except BaseException as e:
        return render_template('error.html', error=e)
    return redirect(url_for('home'))



if __name__ == '__main__':
	app.run(debug=True)
