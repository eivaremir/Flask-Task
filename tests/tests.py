# recordar ver curso de pruebas automatizadas en python
import unittest as ut

from flask import current_app

#importar db y modelos
from app import db, User, Task
from app import create_app

# importar configuraciones
from config import config

class DemoTestCase(ut.TestCase):
    # pasos antes de ejecutar las pruebas
    def setUp(self):
        config_class = config['test']
        self.app = create_app(config_class)
        # ejecutar las pruebas bajo el contexto de la app
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.id=1
    # pasos despues de ejecutar las pruebas
    def tearDown(self):
        # despues de cada prueba, eliminar todos los cambios
        db.session.remove()
        db.drop_all()
        

        self.app_context.pop()

    def test_demo(self):
        self.assertTrue(1==1)

    def test_user_exists(self):
        user = User.get_by_id(self.id)
        self.assertTrue(user is None)
    def test_create_user(self):
        user = User.create_element('username','correo@gmail.com','password')
        self.assertTrue(user.id == self.id)