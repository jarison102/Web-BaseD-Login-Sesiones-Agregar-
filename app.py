from flask import Flask
from flask import render_template, request,redirect #redirect sirve para enviar informacion y mostrar
from flaskext.mysql import MySQL
app= Flask(__name__)
mysql = MySQL()#conexion

app.config['MYSQL_DATABASE_HOST']='localhost'#del 7 al 10 infromacion necesaria para la conexion 
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('admin/sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('admin/sitio/libros.html')

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
    #se ejecuta la instruccion sql
    sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s,%s,%s);"
    datos=(_nombre,_archivo.filename,_url)
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
    cursor.execute("SELECT * FROM `libros` WHERE id=%s",(_id))
    #recuperamos todos estos libros los almacenamos en una variable
    libro=cursor.fetchall()
    conexion.commit()
   #para que me muestre los datos en la terminal
    print(libros)
    
    #borrado de tablas 
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s",(_id))
    conexion.commit()
    return redirect('/admin/libros')





if __name__ == '__main__':
    app.run(debug=True)