from flask_mail import Message
from flask import current_app, render_template
from . import mail, app

from threading import Thread

def welcome_mail(user):
    msg = Message('Bienvenido al proyecto facilito',sender = current_app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.html = render_template("emails/welcome.html", user = user)
    thread = Thread(target=send_async_main, args=[msg])
    thread.start()
    

def send_async_main(message):

    # enviar en contexto tal que se usa un thread
    with app.app_context():
        mail.send(message)