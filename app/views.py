from flask import Blueprint
from flask import render_template, request  # render form fields, handle server requests GET & POST
from flask import flash
from flask import redirect, url_for # funciones de redireccionamiento
from flask import abort #lanzar error 404
from .forms import LoginForm, RegisterForm, TaskForm
from .models import *

from sqlalchemy import exc # for db errors handling

from flask_login import login_user, logout_user, login_required, current_user
from .consts import * 
from .email import *
from . import login_manager




page = Blueprint('page',__name__)

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'),404 # retorna status 200 de exito

@page.route('/')
def index():
    return render_template('index.html',title='Index',active='index')

@page.route("/profile")
@login_required
def profile():
    return render_template("profile/view.html",user=current_user)

@page.route("/profile/<int:profile_id>")
@login_required
def profile_id(profile_id):
    user = User.query.get_or_404(profile_id)
    return render_template("profile/view.html",user=user)
    

@page.route("/logout")
def logout():
    print('Auth: '+str(current_user.is_authenticated))
    logout_user()
    print('Auth: '+str(current_user.is_authenticated))
    flash(LOGOUT)
    return redirect(url_for('.login'))

@page.route("/tasks")
@page.route("/tasks/<int:page>")
@login_required
def tasks(page=1,per_page=2):
    
    pagination = current_user.tasks.paginate(page,per_page)
    tasks = pagination.items
    print('Auth: '+str(current_user.is_authenticated))
    return render_template('task/list.html', title="Tasks",tasks=tasks,pagination=pagination, page=page, active='tasks')

@page.route("/tasks/new", methods=['GET','POST'])
@login_required
def new_task():
    form = TaskForm(request.form)
    if request.method == 'POST':
        if form.validate():
            task = Task.create_element(form.title.data,form.description.data,current_user.id)
            if task:
                flash(TASK_CREATED)
    return render_template('task/new.html',title='Nueva Tarea',form=form, active='new_task')

@page.route("/tasks/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # if the task wasnt created by the user logged in
    if task.user_id != current_user.id:
        abort(404)
    if task.delete_element(task.id):
        flash(TASK_DELETED)
    return redirect(url_for('.tasks'))

@page.route("/tasks/edit/<int:task_id>", methods=['GET','POST'])
@login_required
def edit_task(task_id):
    # obtener la información del task a partir del id
    task = Task.query.get_or_404(task_id)

    # solo el dueño de la tarea puede editar la tarea
    if task.user_id != current_user.id:
        abort(404)

    # instanciar el formulario
    form = TaskForm(request.form,obj=task)
    if request.method == 'POST' and form.validate():
        task = Task.update_element(task.id, form.title.data, form.description.data)
        if task: flash(TASK_UPDATED)
    return render_template("task/edit.html",title="Editar Tarea", form=form)

@page.route("/tasks/show/<int:task_id>")
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("task/show.html", methods=['GET','SHOW'],title="Tarea #"+str(task_id),task=task)

@page.route("/register",methods=['GET','POST'])
def register():
    form = RegisterForm(request.form) 
    if request.method == 'POST' and form.validate(): 
        try:
          
            user = User.create_element(form.username.data,form.password.data,form.email.data)
            welcome_mail(user)
            flash(USER_CREATED)
            #print('Usuario '+str(user.id)+' Creado de forma exitosa')
            
            login_user(user)
            
            if current_user.is_authenticated:
                return redirect(url_for('.tasks'))
        except exc.IntegrityError:
            flash(ERROR_USER_DUPLICATE,'error')
        
        
    print('Auth: '+str(current_user.is_authenticated))
    return render_template("register.html",title='Register', form=form, active='register')    

@page.route("/login",methods=['GET','POST']) # hablitiar metodos para mostrar y crear sesión
def login():
    # request.form es un tipo de dato Form definido en wtforms (Archivo forms.py) con los valores recibidos de un formulario si esta peticion es de tipo post
    # instancia del formulario, con valores del usuario
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))
    form = LoginForm(request.form) 
    
    # if the request to the server is post and validations are correct
    if request.method == 'POST' and form.validate(): 
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(LOGIN)
            if current_user.is_authenticated:
                return redirect(url_for('.tasks'))
        else:
            flash(ERROR_USER_PASSWORD,'error')
        #print("Nueva sesión creada con los valores: " + form.username.data +" "+ form.password.data + " resultado: "+str(current_user.is_authenticated))
    print('Auth: '+str(current_user.is_authenticated))
    
    return render_template("login.html",title='Login', form=form, active = 'login')