from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

# depends on mysqlclient library
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# GENERAR INSTANCIAS
app = Flask(__name__)

bootstrap = Bootstrap(app)
mail = Mail()
csrf = CSRFProtect() # PROTECCION CONTRA ATAQUES CSRF
db = SQLAlchemy() # instancia database
login_manager = LoginManager()

# gather routes from blueprint
from .views import page

# import class for db tables
from .models import *

from .consts import *

def create_app(config):
    # DEFINIR CONFIGURACIONES DEL SERVIDOR
    app.config.from_object(config)

    

    # ASOCIAR INSTANCIA CSRF CON EL SERVER
    csrf.init_app(app)

    #asignacion de bootstrap
    #if not app.config.get('TEST',False):
    #    bootstrap.init_app(app)

    app.app_context().push()
    #login manager - flask-login
    login_manager.init_app(app)
    login_manager.login_view = '.login'
    login_manager.login_message = LOGIN_REQUIRED

    # Servidor de mails
    mail.init_app(app)

    app.register_blueprint(page)

    with app.app_context():
        #iniciar db en el app
        db.init_app(app)

        # crear tablas
        db.create_all()

    return app