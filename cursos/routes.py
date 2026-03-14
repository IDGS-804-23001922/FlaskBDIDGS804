from flask import render_template, request, redirect, url_for
from . import cursos
import forms
from models import db, Alumnos, Curso, Maestros

@cursos.route('/cursos', methods=['GET'])
def listado_cursos():
    lista = Curso.query.all()
    return render_template('cursos/listadoCursos.html', cursos=lista)

@cursos.route('/registrocurso', methods=['GET', 'POST'])
def registrocurso():
    form = forms.CursoForm(request.form)

    if request.method == 'POST':
        c = Curso(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            maestro_id=form.maestro_id.data
        )
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))

    maestros = Maestros.query.all()
    return render_template('cursos/registroCurso.html', form=form, maestros=maestros)

@cursos.route('/modificarcurso', methods=['GET', 'POST'])
def modificarcurso():
    form = forms.CursoForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        c = Curso.query.filter(Curso.id == id).first()
        form.id.data = c.id
        form.nombre.data = c.nombre
        form.descripcion.data = c.descripcion
        form.maestro_id.data = c.maestro_id

    if request.method == 'POST':
        c = Curso.query.filter(Curso.id == form.id.data).first()
        c.nombre = form.nombre.data
        c.descripcion = form.descripcion.data
        c.maestro_id = form.maestro_id.data
        db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))

    maestros = Maestros.query.all()
    return render_template('cursos/modificarCurso.html', form=form, maestros=maestros)

@cursos.route('/eliminarcurso', methods=['GET', 'POST'])
def eliminarcurso():
    form = forms.CursoForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        c = Curso.query.filter(Curso.id == id).first()
        form.id.data = c.id
        form.nombre.data = c.nombre
        form.descripcion.data = c.descripcion
        form.maestro_id.data = c.maestro_id

    if request.method == 'POST':
        c = Curso.query.filter(Curso.id == form.id.data).first()
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('cursos.listado_cursos'))

    return render_template('cursos/eliminarCurso.html', form=form)

@cursos.route('/detallescurso', methods=['GET'])
def detallescurso():
    id = request.args.get('id')
    c = Curso.query.filter(Curso.id == id).first()
    return render_template('cursos/detallesCurso.html', curso=c)

@cursos.route('/inscribir', methods=['GET', 'POST'])
def inscribir():
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')

        alumno = Alumnos.query.get(alumno_id)
        curso = Curso.query.get(curso_id)

        if alumno and curso:
            if alumno not in curso.alumnos:
                curso.alumnos.append(alumno)
                db.session.commit()

        return redirect(url_for('cursos.listado_cursos'))

    alumnos = Alumnos.query.all()
    cursos_lista = Curso.query.all()
    return render_template('cursos/inscribir.html', alumnos=alumnos, cursos=cursos_lista)

@cursos.route('/consultas', methods=['GET'])
def principal_consultas():
    return render_template('cursos/principal_consultas.html')

@cursos.route('/consultascursos', methods=['GET'])
def consultas_cursos():
    buscar_curso = request.args.get('buscar_curso', '')
    cursos_db = Curso.query.all()
    cursos_lista = []

    if buscar_curso == '':
        cursos_lista = cursos_db
    else:
        for curso in cursos_db:
            if buscar_curso.lower() in curso.nombre.lower():
                cursos_lista.append(curso)

    return render_template('cursos/consultasCursos.html', cursos=cursos_lista, buscar_curso=buscar_curso)

@cursos.route('/consultas/cursosdetalles', methods=['GET'])
def detalle_consulta_curso():
    id = request.args.get('id')
    curso = Curso.query.filter(Curso.id == id).first()
    return render_template('cursos/detalleConsultaCurso.html', curso=curso)

@cursos.route('/consultasalumnos', methods=['GET'])
def consultas_alumnos():
    buscar_alumno = request.args.get('buscar_alumno', '')
    alumnos_db = Alumnos.query.all()
    alumnos_lista = []

    if buscar_alumno == '':
        alumnos_lista = alumnos_db
    else:
        for alumno in alumnos_db:
            nombre_completo = alumno.nombre + " " + alumno.apellidos

            if buscar_alumno.lower() in alumno.nombre.lower():
                alumnos_lista.append(alumno)
            elif buscar_alumno.lower() in alumno.apellidos.lower():
                alumnos_lista.append(alumno)
            elif buscar_alumno.lower() in nombre_completo.lower():
                alumnos_lista.append(alumno)

    return render_template('cursos/consultasAlumnos.html', alumnos=alumnos_lista, buscar_alumno=buscar_alumno)

@cursos.route('/consultas/aludetalles', methods=['GET'])
def detalle_consulta_alumno():
    id = request.args.get('id')
    alumno = Alumnos.query.filter(Alumnos.id == id).first()
    return render_template('cursos/detalleConsultaAlumno.html', alumno=alumno)