from decouple import config
class Config:
    # DEFINIR LLAVE SECRETA PARA GENERAR TOKENS PARA FORMULARIOS
    SECRET_KEY = '12345678'
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:eemp10200@localhost/project_web_facilito' # conexion a la dbs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME ='eivaremir@gmail.com'
    MAIL_PASSWORD =config('PASSWD')
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:eemp10200@localhost/project_web_facilito_test' # conexion a la dbs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST = True
    
config ={
    'development':DevelopmentConfig,
    'default':DevelopmentConfig,
    'test':TestConfig
}
