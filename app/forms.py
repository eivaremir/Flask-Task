from wtforms import Form
from wtforms import validators #validaciones de formularios
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User

def username_validator(form, field):
    if field.data == 'pendejo' or field.data=='PENDEJO':
        raise validators.ValidationError('El nombre de usuario no cumple con los estándares de la compañía')

# proteccion anti bots
def length_honeypot(form,field):
    if len(field.data)>0:
        raise validators.ValidationError('Registro no permitido')


class TaskForm(Form):
    title = StringField('Titulo',[
        validators.length(min=4,max=50, message = 'Titulo debe estar entre 4 y 50 caracteres'),
        validators.DataRequired(message = 'El titulo es requerido.')
        
    ])
    description = TextAreaField('Descripción',[
        validators.DataRequired(message='La descripción es requerida')
    ], render_kw={'rows':5})

class LoginForm(Form):
    #campos con las respectivas validaciones
    username = StringField('Username',[validators.length(min=8,max=50,message='El nombre de usuario debe ser mayor a 8 caracteres')])
    password = PasswordField('Password',[validators.Required()])

class RegisterForm(Form):
    #campos con las respectivas validaciones
    honeypot = HiddenField("",[length_honeypot])
    email = EmailField('E-mail',[
        validators.Required(message='Debe proveer su correo electrónico'),
        validators.length(min=6,max=100),
        validators.Email(message='Ingrese un email válido')
    ])
    username = StringField('Username',[
        validators.length(min=8,max=50,message='El nombre de usuario debe ser mayor a 8 caracteres'),
        username_validator
    ])
    password = PasswordField('Password',[validators.Required(), validators.EqualTo('confirm_password', message='las contraseñas deben coincidir')])
    confirm_password = PasswordField('Confirm Password',[validators.Required()])
    accept = BooleanField('',[validators.DataRequired()])

    # testear como saber cuando se hace referencia al campo especificamente
    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError("El usuario ya se encuentra registrado")
    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError("El email ya se encuentra registrado")
    
    def validate(self):
        # recomendado ejecutar las validaciones previamente definidas
        if not Form.validate(self): return False

        # el campo password debe ser mayor a 3 caracteres
        if len(self.password.data)<3:
            self.password.errors.append('El password debe ser mayor a 3 caracteres')
            return False
        
        return True