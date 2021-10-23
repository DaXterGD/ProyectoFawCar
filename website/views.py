from flask import Blueprint, render_template, request, redirect, flash, session, Response, make_response
from .models import Usuarios, Inventario, Proveedores,db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from markupsafe import escape
import base64
from PIL import Image
from io import BytesIO



views = Blueprint("views", __name__)

@views.route("/")
def ingreso():
    return render_template("ingreso.html")

@views.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username_login = escape(request.form["user"])
        password = escape(request.form["pass"])
        log=Usuarios.query.filter_by(usuario=username_login).first()

        if log:
            if log.check_password(password):
                session["user"]=log.usuario
                session["rol"]=log.rol
                session["nombre"]=log.nombre
                flash("Bienvenido %s" % (session["nombre"]),"info")
                return redirect("inicio")
        else:
            flash("Usuario o contraseña incorrectos","danger")
            return redirect("/")
    else:
        flash("el metodo no fue POST")
        return redirect("/")
          

@views.route("/logout")
def logout():
    session.clear()
    flash("has cerrado sesion","success")
    return redirect("/")
  

@views.route("/inicio")
def inicio():
    return render_template("inicio.html")

@views.route("/usuarios")
def usuarios():
    if "user" in session:
        if session["rol"]=="superadministrador" or session["rol"]=="administrador":
            return render_template('usuarios.html',usuarios=Usuarios.query.all())
        else:
            flash("no tienes permiso para acceder a esta pagina","danger")
            return redirect("inicio")
    flash("Debes iniciar sesion","danger")
    return redirect("/")

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
        nombre = escape(request.form["usuarios_nombre"])
        apellido =escape(request.form["usuarios_apellido"])
        usuario =escape(request.form["usuarios_usuario"])
        clave =escape(request.form["usuarios_clave"])
        confirmar =escape(request.form["usuarios_confirmar"])
        rol =escape(request.form["usuarios_rol"])
        cedula =escape(request.form["usuarios_cedula"])
        correo =escape(request.form["usuarios_correo"])
        cargo =escape(request.form["usuarios_cargo"])
        imagen =request.files["usuarios_imagen"]
        filename=secure_filename(imagen.filename)
        mimetype=imagen.mimetype
        
        if clave==confirmar:
            user=Usuarios(nombre=nombre,apellido=apellido,usuario=usuario,rol=rol,cedula=cedula,correo=correo,cargo=cargo,imagen=imagen.read(),name=filename,mimetype=mimetype)
            user.set_password(clave)
            db.session.add(user)
            db.session.commit()
            flash("usuario agregado exitosamente","info")
            return redirect("/usuarios")


@views.route("/usuarios/search", methods=['POST'])
def usuarios_search():
    b=request.form["searchbox"]
    if request.form.get("opt")=="nombre":
        img = Usuarios.query.filter_by(nombre=b)
        for imgs in img:
            x= Image.open(BytesIO(imgs.imagen))
            w=BytesIO()
            x=x.resize((480,480))
            x.save(w,'jpeg')
            imgcod=base64.b64encode(w.getvalue())
            return render_template("usuarios.html",usuarios=img,img=imgcod.decode('utf-8'))
        return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(nombre=b),img=img)
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
def convert_data(data, file_name):
    # Convert binary format to images or files data
    with open(file_name, 'wb') as file:
        file.write(data)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")