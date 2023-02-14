from flask import Flask
from flask import render_template

app= Flask(__name__)

@app.route('/')
def inicio():
    return render_template('admin/sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('admin/sitio/libros.html')

@app.route('/nosotros')
def nosotros():
    return render_template('admin/sitio/nosotros.html')



if __name__ == '__main__':
    app.run(debug=True)