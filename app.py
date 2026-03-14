from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from flask_migrate import Migrate
from maestros.routes import maestros
from cursos.routes import cursos


from models import db
from models import Alumnos
from models import Curso
from models import Inscripcion

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(maestros)
app.register_blueprint(cursos)


@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route("/alumnos", methods=['GET', 'POST'])
def principal():
    create_form = forms.UserForm()
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/alumnosRe', methods=['GET', 'POST'])
def alumnosRe():
    alumno_class = forms.UserForm()

    if alumno_class.validate_on_submit():
        alum = Alumnos(
            nombre=alumno_class.nombre.data,
            apellidos=alumno_class.apellidos.data,
            email=alumno_class.email.data,
            telefono=alumno_class.telefono.data
        )

        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('principal'))

    return render_template("Alumnos.html", form=alumno_class)


@app.route('/detalles', methods=['GET', 'POST'])
def detalles():
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alumn1:
            nombre = alumn1.nombre
            apellidos = alumn1.apellidos
            email = alumn1.email
            telefono = alumn1.telefono
            return render_template("detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono)

    return redirect(url_for('principal'))


@app.route('/modificar', methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm()

    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alumn1:
            create_form.id.data = alumn1.id
            create_form.nombre.data = alumn1.nombre
            create_form.apellidos.data = alumn1.apellidos
            create_form.email.data = alumn1.email
            create_form.telefono.data = alumn1.telefono

    if create_form.validate_on_submit():
        id = create_form.id.data
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alumn1:
            alumn1.nombre = create_form.nombre.data.rstrip()
            alumn1.apellidos = create_form.apellidos.data
            alumn1.email = create_form.email.data
            alumn1.telefono = create_form.telefono.data
            db.session.commit()

        return redirect(url_for('index.html'))

    return render_template("modificar.html", form=create_form)

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm()

    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alumn1:
            create_form.id.data = alumn1.id
            create_form.nombre.data = alumn1.nombre
            create_form.apellidos.data = alumn1.apellidos
            create_form.email.data = alumn1.email
            create_form.telefono.data = alumn1.telefono

    if create_form.validate_on_submit():

        id = create_form.id.data
        alumn = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        
        inscripciones = db.session.query(Inscripcion).filter(Inscripcion.alumno_id == id).all()

        if len(inscripciones) > 0:
            flash("No se puede eliminar el alumno porque está inscrito en un curso")
            return render_template("eliminar.html", form=create_form)

        if alumn:
            db.session.delete(alumn)
            db.session.commit()

        flash("Alumno eliminado correctamente")
        return redirect(url_for('principal'))

    return render_template("eliminar.html", form=create_form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)