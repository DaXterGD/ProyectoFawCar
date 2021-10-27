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
        
        if len(username_login) == 0:
            flash("Escribe tu nombre de usuario", "danger")  
        elif len(password) == 0:
            flash("Escribe tu contraseña", "danger")  
        else:
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
    
    #flash("el metodo no fue POST")
    return redirect("/")
          

@views.route("/logout")
def logout():
    if "user" in session:
        session.clear()
        flash("has cerrado sesion","success")
        return redirect("/")
  

@views.route("/inicio")
def inicio():
    if "user" in session:
        return render_template("inicio.html")
    flash("Debes iniciar sesion","danger")
    return redirect("/")

@views.route("/usuarios")
def usuarios():
    if "user" in session:
        if session["rol"]=="superadministrador" or session["rol"]=="administrador":
            usuarios=Usuarios.query.all()
            for usuario in usuarios:
                if usuario.imagen:
                    w=BytesIO()
                    x= Image.open(BytesIO(usuario.imagen))
                    # x=x.resize((80,80))
                    x.save(w, usuario.mimetype)
                    imgcod=base64.b64encode(w.getvalue())
                    usuario.imagen=imgcod.decode('utf-8')
                    # usuario.clave = check_password_hash(usuario.clave)
            return render_template('usuarios.html',usuarios=usuarios)
        else:
            flash("no tienes permiso para acceder a esta pagina","danger")
            return redirect("inicio")
    flash("Debes iniciar sesion","danger")
    return redirect("/")

@views.route("/inventario")
def inventario():
    if "user" in session: #VERIFICAR SI SE INICIO SESION
        if session["rol"]=="superadministrador" or session["rol"]=="administrador": #VERIFICAR SI EL ROL TIENE ACCESO
            inventarios = Inventario.query.all()
            for inventario in inventarios:
                if inventario.imagen:
                    w=BytesIO()
                    x= Image.open(BytesIO(inventario.imagen))
                    x.save(w,inventario.mimetype)
                    imgcod=base64.b64encode(w.getvalue())
                    inventario.imagen=imgcod.decode('utf-8')
            return render_template('inventario.html',inventario=inventarios)
        else: #SI EL ROL NO TIENE ACCESO SE NOTIFICA AL USUARIO Y SE LE ENVIA AL INICIO
            flash("no tienes permiso para acceder a esta pagina","danger")
            return redirect("inicio")
    #SI NO HAY SESION, SE DEBE INICIAR SESION
    flash("Debes iniciar sesion","danger")
    return redirect("/")

@views.route("/proveedores")
def proveedor():
        if "user" in session: #VERIFICAR SI SE INICIO SESION no cambiar
            if session["rol"]=="superadministrador" or session["rol"]=="administrador": #VERIFICAR SI EL ROL TIENE ACCESO
                proveedores = Proveedores.query.all()
                for proveedor in proveedores:
                    if proveedor.imagen:
                        w=BytesIO()
                        x= Image.open(BytesIO(proveedor.imagen))
                        x.save(w,proveedor.mimetype)
                        imgcod=base64.b64encode(w.getvalue())
                        proveedor.imagen=imgcod.decode('utf-8')
                return render_template('proveedores.html',proveedor= proveedores)
            else: #SI EL ROL NO TIENE ACCESO SE NOTIFICA AL USUARIO Y SE LE ENVIA AL INICIO
                flash("no tienes permiso para acceder a esta pagina","danger")
                return redirect("inicio")
        #SI NO HAY SESION, SE DEBE INICIAR SESION
        flash("Debes iniciar sesion","danger")
        return redirect("/")


# CRUD ROUTES
# USUARIOS
@views.route("/usuarios/add", methods=['POST'])
def usuarios_add():
    # if request.method=='POST':
        nombre = escape(request.form["usuarios_nombre"]).lower()
        apellido =escape(request.form["usuarios_apellido"]).lower()
        usuario =escape(request.form["usuarios_usuario"])
        clave =escape(request.form["usuarios_clave"]).lower()
        confirmar =escape(request.form["usuarios_confirmar"]).lower()
        rol =escape(request.form["usuarios_rol"]).lower()
        cedula =escape(request.form["usuarios_cedula"]).lower()
        correo =escape(request.form["usuarios_correo"]).lower()
        cargo =escape(request.form["usuarios_cargo"]).lower()
        imagen =request.files["usuarios_imagen"]
        filename=secure_filename(imagen.filename)
        mimetype= imagen.mimetype
        mimetype=mimetype.split("/")
        mimetype=mimetype[1]
        
        if clave==confirmar:
            user= Usuarios(nombre=nombre,apellido=apellido,usuario=usuario,rol=rol,cedula=cedula,correo=correo,cargo=cargo,imagen=imagen.read(),name=filename,mimetype=mimetype)
            user.set_password(clave)
            db.session.add(user)
            db.session.commit()
            flash("usuario agregado exitosamente","info")
            return redirect("/usuarios")
        else:
            flash("Las contraseñas no coinciden", "warning")
            return redirect("/usuarios")


@views.route("/usuarios/search", methods=['POST'])
def usuarios_search():
    b="%{}%".format(request.form["searchbox"])
    h=request.form.get("opt")

    usuarios = Usuarios.query.filter(getattr(Usuarios, h).ilike(b))

    for usuario in usuarios:

        if usuario.imagen:
            tipo =usuario.mimetype
            w=BytesIO()
            x= Image.open(BytesIO(usuario.imagen))
            # x=x.resize((80,80))
            x.save(w,tipo)
            imgcod=base64.b64encode(w.getvalue())
            usuario.imagen=imgcod.decode('utf-8')
            return render_template('usuarios.html',usuarios=usuarios)
        # return render_template("usuarios.html",usuarios=Usuarios.query.filter_by(nombre=b))
    
    flash("usuario no encontrado")
    return render_template('usuarios.html',usuarios=Usuarios.query.all())


@views.route("/usuarios/update", methods=['POST'])
def usuarios_update():
    nombre_usuario=escape(request.form["usuarios_usuario"])
    user=Usuarios.query.filter_by(usuario=nombre_usuario).first()

    user.nombre = escape(request.form["usuarios_nombre"])
    user.apellido =escape(request.form["usuarios_apellido"])
    # user.usuario =escape(request.form["usuarios_usuario"])
    user.clave =escape(request.form["usuarios_clave"])
    # user.confirmar =escape(request.form["usuarios_confirmar"]).lower()
    user.rol =escape(request.form["usuarios_rol"])
    user.cedula =escape(request.form["usuarios_cedula"])
    user.correo =escape(request.form["usuarios_correo"]).lower()
    user.cargo =escape(request.form["usuarios_cargo"])
    user.imagen =request.files["usuarios_imagen"].read()
    user.name=secure_filename(user.imagen.filename)
    user.mimetype=user.imagen.mimetype
    db.session.commit()
    return redirect("/usuarios")

@views.route("/usuarios/delete", methods=['POST'])
def usuarios_delete():
    nombre_usuario =escape(request.form["usuarios_usuario"])

    if len(nombre_usuario) == 0:
        flash("Para eliminar un usuario, primero ingresa su <nombre de usuario>", "danger")
        return redirect("/usuarios")
    else:
        usuario = Usuarios.query.filter_by(usuario=nombre_usuario).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            flash("Usuario eliminado", "success")
            return redirect("/usuarios")
        else:
            flash("Usuario no encontrado", "warning")
            return redirect("/usuarios")


# INVENTARIO
@views.route("/inventario/add", methods=['POST'])
def inventario_add():
        marca = escape(request.form["inventario_marca"]).lower()
        modelo =escape(request.form["inventario_modelo"]).lower()
        cantidad =escape(request.form["inventario_cantidad"])
        fecha_salida =escape(request.form["inventario_fecha_salida"]).lower()
        cantidad_minima =escape(request.form["inventario_cantidad_minima"]).lower()
        imagen =request.files["inventario_imagen"]
        filename=secure_filename(imagen.filename)
        mimetype= imagen.mimetype
        mimetype=mimetype.split("/")
        mimetype=mimetype[1]

        prod=Inventario(marca=marca,modelo=modelo,cantidad=cantidad,fecha_salida=fecha_salida,cantidad_minima=cantidad_minima,imagen=imagen.read(),name=filename,mimetype=mimetype)
        db.session.add(prod)
        db.session.commit()
        flash("Articulo agregado exitosamente","info")
        return redirect("/inventario")
  

@views.route("/inventario/update", methods=['POST'])
def inventario_update():
    id_producto=escape(request.form["inventarios_id"])
    prod=Inventario.query.filter_by(usuario=id_producto).first()

    prod.marca = escape(request.form["inventario_marca"]).lower()
    prod.modelo =escape(request.form["inventario_modelo"]).lower()
    prod.cantidad =escape(request.form["inventario_cantidad"])
    prod.fecha_salida =escape(request.form["inventario_fecha_salida"]).lower()
    prod.cantidad_minima =escape(request.form["inventario_cantidad_minima"]).lower()
    prod.imagen =request.files["inventario_imagen"].read()
    prod.filename=secure_filename(prod.imagen.filename)
    prod.mimetype=prod.imagen.mimetype
    prod.db.session.commit()
    return redirect("/inventarios")


@views.route("/inventario/delete", methods=['POST'])
def inventario_delete():
    
    id_articulo =escape(request.form["inventario_id"])

    if len(id_articulo) == 0:
        flash("Seleccione un articulo para eliminarlo", "danger")
        return redirect("/inventario")
    else:
        articulo = Inventario.query.filter_by(id=id_articulo).first()
        if articulo:
            db.session.delete(articulo)
            db.session.commit()
            flash("Articulo eliminado", "success")
            return redirect("/inventario")
        else:
            flash("Articulo no encontrado", "warning")
            return redirect("/inventario")

    


@views.route("inventario/search", methods=['POST'])
def inventario_search():
    b="%{}%".format(request.form["searchbox"])
    h=request.form.get("opt_inventario")

    inventarios = Inventario.query.filter(getattr(Inventario, h).ilike(b))

    for inventario in inventarios:

        if inventario.imagen:
            tipo =inventario.mimetype
            w=BytesIO()
            x= Image.open(BytesIO(inventario.imagen))
            # x=x.resize((80,80))
            x.save(w,tipo)
            imgcod=base64.b64encode(w.getvalue())
            inventario.imagen=imgcod.decode('utf-8')
            return render_template('inventario.html',inventario=inventarios)
    
    flash("inventario no encontrado")
    return render_template('proveinventariosedor.html',inventario=Inventario.query.all())

# PROVEEDORES
@views.route("/proveedores/add", methods=['POST'])
def proveedores_add():
    empresa = escape(request.form["proveedores_empresa"])
    contacto =escape(request.form["proveedores_contacto"])
    telefono =escape(request.form["proveedores_telefono"])
    direccion =escape(request.form["proveedores_direccion"])
    correo =escape(request.form["proveedores_correo"])
    imagen =request.files["imgproveedor"]
    filename=secure_filename(imagen.filename)
    mimetype= imagen.mimetype
    mimetype=mimetype.split("/")
    mimetype=mimetype[1]
        

    proveedor = Proveedores(empresa=empresa,contacto=contacto,telefono=telefono,direccion=direccion,correo=correo,imagen=imagen.read(),name=filename,mimetype=mimetype)
    db.session.add(proveedor)
    db.session.commit()
    flash("Proveedor agregado exitosamente","info")
    return redirect("/proveedores")


@views.route("/proveedores/update", methods=['POST'])
def proveedores_update():

    nombre_usuario=escape(request.form["proveedor_usuario"])
    provee=Proveedores.query.filter_by(usuario=nombre_usuario).first()

    provee.apellido =escape(request.form["proveedor_apellido"])
    # provee.usuario =escape(request.form["proveedor_usuario"])
    provee.clave =escape(request.form["proveedor_clave"])
    # provee.confirmar =escape(request.form["proveedor_confirmar"]).lower()
    provee.rol =escape(request.form["proveedor_rol"])
    provee.cedula =escape(request.form["proveedor_cedula"])
    provee.correo =escape(request.form["proveedor_correo"]).lower()
    provee.cargo =escape(request.form["proveedor_cargo"])
    provee.imagen =request.files["proveedor_imagen"].read()
    provee.name=secure_filename(provee.imagen.filename)
    provee.mimetype=provee.imagen.mimetype
    db.session.commit()
    return redirect("/proveedores")

@views.route("/proveedores/delete", methods=['POST'])
def proveedores_delete():
    return redirect("/proveedores")

@views.route("/proveedores/search", methods=['POST'])
def proveedores_search():
    b="%{}%".format(request.form["searchbox"])
    h=request.form.get("opt_proveedores")

    productos = Inventario.query.filter(getattr(Inventario, h).ilike(b))

    for producto in productos:

        if producto.imagen:
            tipo =producto.mimetype
            w=BytesIO()
            x= Image.open(BytesIO(producto.imagen))
            # x=x.resize((80,80))
            x.save(w,tipo)
            imgcod=base64.b64encode(w.getvalue())
            producto.imagen=imgcod.decode('utf-8')
            return render_template('proveedor.html',inventario=productos)
        # return render_template("proveedor.html",proveedor=proveedor.query.filter_by(nombre=b))
    
    flash("usuario no encontrado")
    return render_template('proveedor.html',inventario=Inventario.query.all())


@views.route("/prueba")
def prueba():
    return render_template("prueba.html")