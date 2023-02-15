from flask import Flask
#redirect sirve para enviar informacion y mostrar
from flaskext.mysql import MySQL
from flask import render_template, request,redirect,session
from flaskext.mysql import MySQL
from datetime import datetime 
from flask import send_from_directory #esto nos sirve informacion directamente de la imagen
import os
from werkzeug.security import generate_password_hash, check_password_hash

app= Flask(__name__)
app.secret_key="Stivur"
mysql = MySQL()#conexion

app.config['MYSQL_DATABASE_HOST']='localhost'#del 7 al 10 infromacion necesaria para la conexion 
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('admin/sitio/index.html')

@app.route('/img/<imagen>') #lo que hace que se muestre la imagen es todo esto de la 21 a 24
def imgenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/admin/sitio/img'),imagen)

@app.route('/libros')
def libros():
    conexion=mysql.connect() 
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros` ")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/sitio/libros.html',libros=libros)

@app.route('/nosotros')
def nosotros():
    return render_template('admin/sitio/nosotros.html')

@app.route('/login')
def login():
    return render_template('admin/sitio/login.html')


@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _Nombre = request.form['txtNombre']
    _SegundoNombre = request.form['txtSegundoNombre']
    _Username = request.form['txtUsername']
    _Ciudad = request.form['txtCiudad']
    _Estado = request.form['txtEstado']
    _Pais = request.form ['txtPais']

    print(_Nombre)
    print(_SegundoNombre)
    print(_Username)
    print(_Ciudad)
    print(_Estado)
    print(_Pais)
    if _Nombre=="Jarison" and _SegundoNombre =="Stived" and _Username =="Stivur" and _Ciudad=="Bogota" and _Estado=="Activo" and _Pais =="Colombia":
        session["login"]=True
        session["Nombre"]="Administrador"
        return redirect ("/admin/")
    return render_template("/admin/login.html")


    
@app.route('/admin/libros')
def admin_libros():
    conexion=mysql.connect()#esto es para conectar directamente con la base de datos 
    cursor=conexion.cursor()
    #instruccion de seleccion sql
    cursor.execute("SELECT * FROM `libros` ")
    #recuperamos todos estos libros los almacenamos en una variable
    libros=cursor.fetchall()
    conexion.commit()
   #para que me muestre los datos en la terminal
    print(libros)
    print(conexion)
    return render_template('admin/libros.html',libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])#recepcionamos los datos atravez del metodo post
def admin_libros_guardar():
    _nombre=request.form['txtNombre']
    _url =request.form['txtUrl']
    _archivo = request.files['txtImagen']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/admin/sitio/img/"+nuevoNombre)
    #se ejecuta la instruccion sql
    sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s,%s,%s);"
    datos=(_nombre,nuevoNombre,_url)
    #se habre la conexion
    conexion = mysql.connect()
    #se crear un cursor
    cursor=conexion.cursor()
    #ese cursor se ejecuta en la instruccion sql
    cursor.execute(sql,datos)
    #alfinal se hace creacion de todo esto
    conexion.commit()
    #imprimimos solo el valor que escribimos
    print(_nombre)#este request lo utilizamos para recolectar y el form es del formulario
    print(_url)
    print(_archivo)
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libro_borrar():
    _id=request.form['txtID']
    print(_id)
    conexion=mysql.connect()#esto es para conectar directamente con la base de datos 
    cursor=conexion.cursor()
    #instruccion de seleccion sql
    cursor.execute("SELECT imagen FROM `libros` WHERE id=%s",(_id))
    #recuperamos todos estos libros los almacenamos en una variable
    libro=cursor.fetchall()
    conexion.commit()
   #para que me muestre los datos en la terminal
    print(libro)
    #valida que hay una imagen y si hay la borra
    if os.path.exists("templates/admin/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/admin/sitio/img/"+str(libro[0][0]))
    
    #borrado de tablas 
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s",(_id))
    conexion.commit()
    return redirect('/admin/libros')





if __name__ == '__main__':
    app.run(debug=True)