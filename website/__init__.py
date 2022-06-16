import logging
import os
from os import path

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from website import inserting_selecting_data

db = SQLAlchemy()
Main_database = 'Main.db'
mail = Mail()

def create_app():
    """
    creating the flask app for the webpage.

    Returns
    -------
    Nothing will be return 

    
    @author : Mashhood Manzoor
    @author : Harry Webster
    @author : Harveen Chada
    @author : Shing him Yip
    
    """
   
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ahfguifahfkjglhafkjghlksf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Main_database}'
    app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] =  ''
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    delete_database()
    create_database(app)


    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_database(app):
    """
    inserting the data form txt file.

    Parameters
    ----------
    app : flask.app.Flask
        specific the flask app programme need to use .

    Returns
    -------
    Nothing will be returned

    @author : Shing him Yip 

    """
    logging.debug('Creating database')
    if not path.exists('website/' + Main_database):
        db.create_all(app=app)
        inserting_selecting_data.initialise_data(app, "website/resources/user.txt")
        inserting_selecting_data.initialise_data(app, "website/resources/Type.txt")
        inserting_selecting_data.initialise_data(app, "website/resources/Item.txt")
        inserting_selecting_data.initialise_data(app, "website/resources/Trait.txt")
        print('Created database!')


def delete_database():
    """
    delete all the database and create it again ,and let the programme to insert the data again.
    
    Returns
    -------
    Nothing will be returned

    @author : Shing him Yip
    
    """
    logging.debug('removing the database')
    if os.path.exists('website/' + Main_database):
        os.remove('website/' + Main_database)
        # os.system("rm -rf *.db")

