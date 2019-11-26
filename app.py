#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, BuscarForm


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios.csv', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


@app.route('/clientes')
def clientes():
    if 'username' in session:
        with open('clientes.csv', 'r', encoding='utf-8') as archivo:
            archivo_csv = csv.reader(archivo)                
            encabezado = next(archivo_csv)                                
            return render_template('clientes.html', cabeza=encabezado, cuerpo=archivo_csv)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route("/buscando_paises", methods=["GET", "POST"])
def buscando_paises():
    if "username" in session:
        formulario = BuscarForm()
        if formulario.validate_on_submit():
            paisbuscado = formulario.buscar.data.capitalize()
            with open("clientes.csv", encoding="utf8") as archivo:
                archivo_csv = csv.reader(archivo)
                listapaises = []
                for l in archivo_csv:
                    if l[3] not in listapaises:
                        if paisbuscado == l[3]:
                            listapaises.append(l[3])
                if not listapaises:
                    flash('No se encontraron clientes de ese pais')
                return render_template("busqueda_pais.html", form=formulario, listapaises=listapaises)
        return render_template("busqueda_pais.html", form=formulario)
    return redirect(url_for("ingresar"))


@app.route("/buscado_pais/<l>")
def buscado_pais(l):
    if "username" in session:
        with open("clientes.csv", encoding="utf8") as archivo:
            archivo_csv = csv.reader(archivo)
            encabezado = next(archivo_csv)
            listaclientes = []
            for cliente in archivo_csv:
                if cliente[3] == l:
                    listaclientes.append(cliente)
            return render_template("clientes_paises.html", listaclientes=listaclientes, cabeza=encabezado)
    return redirect(url_for("ingresar")) 


if __name__ == "__main__":
    app.run(debug=True)