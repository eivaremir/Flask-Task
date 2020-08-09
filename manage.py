from app import create_app
from app import db, User, Task # import for shell
from flask_script import Manager, Shell
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

config_class = config['development']


def make_shell_context():
    return dict(app=app,db=db,User=User,Task=Task)

# INSTANCIA DE LA APP CON LAS CONFIGURACIONES
app = create_app(config_class)

migrate=Migrate(app,db)

if __name__=='__main__':
    manager = Manager(app)

    # add command for shell usage
    manager.add_command('shell',Shell(make_context=make_shell_context))
    manager.add_command('db',MigrateCommand)
    # definir comando como funcion
    @manager.command
    def test():
        import unittest as ut
        tests = ut.TestLoader().discover('tests')
        ut.TextTestRunner().run(tests)
        
    manager.run()
