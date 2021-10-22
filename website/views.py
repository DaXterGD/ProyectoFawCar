from os import name
from flask import Blueprint, render_template, request, redirect, flash, session
from .models import Usuarios, Inventario, Proveedores,db
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint("views", __name__)

@views.route("/")
def ingreso():
    return render_template("ingreso.html")

@views.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username_login = request.form["user"]
        password = request.form["pass"]
        log=Usuarios.query.filter_by(usuario=username_login).first()

        if log:
            if log.check_password(password):
                session["user"]=log.usuario
                session["rol"]=log.rol
                return redirect("inicio")
            # else:
            #     flash("contraseña incorrecta")
            #     return redirect("/")
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect("/")
    else:
        flash("el metodo no fue POST")
        return redirect("/")
        



    # if len(username_login) == 0:
    #     flash("Escribe tu nombre de usuario", category="error")  
    # elif len(password) == 0:
    #     flash("Escribe tu contraseña", category="error")  
    # else:
    #     return redirect("inicio")

    # return redirect("/")    

@views.route("/inicio")
def inicio():
    return render_template("inicio.html")

@views.route("/usuarios")
def usuarios():
    return render_template('usuarios.html',usuarios=Usuarios.query.all())

@views.route("/inventario")
def inventario():

    return render_template('inventario.html')

@views.route("/proveedores")
def proveedor():
    return render_template('proveedores.html')


# CRUD ROUTES
# USUARIOS
@views.route("/usuarios/add", methods=['POST'])
def usuarios_add():
    # if request.method=='POST':
    
        nombre = request.form["usuarios_nombre"]
        apellido = request.form["usuarios_apellido"]
        usuario = request.form["usuarios_usuario"]
        clave = request.form["usuarios_clave"]
        confirmar = request.form["usuarios_confirmar"]
        rol = request.form["usuarios_rol"]
        cedula = request.form["usuarios_cedula"]
        correo = request.form["usuarios_correo"]
        cargo = request.form["usuarios_cargo"]
        # imagen = request.files["input"]
        
        if clave==confirmar:
            user=Usuarios(nombre=nombre,apellido=apellido,usuario=usuario,rol=rol,cedula=cedula,correo=correo,cargo=cargo)
            user.set_password(clave)
            db.session.add(user)
            db.session.commit()
            flash("usuario agregado exitosamente")
            return redirect("/usuarios")


@views.route("/usuarios/search", methods=['POST'])
def usuarios_search():
    b=request.form["searchbox"]
    if request.form.get("opt")=="nombre":
        return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(nombre=b))
    elif request.form.get("opt")=="usuario":
        return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(usuario=b))
    elif request.form.get("opt")=="cargo":
        return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(cargo=b))
    elif request.form.get("opt")=="cedula":
        return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(cedula=b))
    
    flash("usuario no encontrado")
    return render_template('usuarios.html',usuarios=Usuarios.query.all())

@views.route("/usuarios/update", methods=['POST'])
def usuarios_update():
    pass

@views.route("/usuarios/delete", methods=['POST'])
def usuarios_delete():
    return redirect("/usuarios")


# INVENTARIO
@views.route("/inventario/add", methods=['POST'])
def inventario_add():
    return redirect("/inventario")

@views.route("/inventario/update", methods=['POST'])
def inventario_update():
    pass

@views.route("/inventario/delete", methods=['POST'])
def inventario_delete():
    return redirect("/inventario")


# PROVEEDORES
@views.route("/proveedores/add", methods=['POST'])
def proveedores_add():
    pass

@views.route("/proveedores/update", methods=['POST'])
def proveedores_update():
    pass

@views.route("/proveedores/delete", methods=['POST'])
def proveedores_delete():
    return redirect("/proveedores")


@views.route("/prueba")
def prueba():
    
    return render_template('prueba.html',x=Usuarios.query.all())