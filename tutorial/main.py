from flask import Flask
from flask import render_template, request

app = Flask(__name__) # enviar contexto

@app.before_request
def before_request():
    print("Antes de la peticion")

@app.after_request
def after_request(response):
    print("despues de la peticion")
    return response

@app.route('/') #creamos ruta decorando index
def index():
    name = 'Eivar'
    course = 'Python'
    ispremium = False
    courses = ['python', 'ruby','java']
    return render_template('index.html',username=name,
                                        course_name=course,
                                        is_premium = ispremium,
                                        Courses=courses)
                                        
    #return "<h1>Hola mundo desde el servidor de flask</h1>"

@app.route('/usuario/<last_name>/<name>/<int:age>')
def usuario(last_name,name,age):
    return 'Hola '+name+" "+last_name+" "+str(age)

@app.route('/datos')
def datos():
    nombre = request.args.get('nombre') # diccionario
    curso =  request.args.get('curso') # diccionario
    return 'listado de datos '+nombre+ " "
@app.route('/about')
def about():
    print("estamos en el about")
    return render_template('about.html')
if __name__ =='__main__':
    app.run(port=4000,debug=True)
