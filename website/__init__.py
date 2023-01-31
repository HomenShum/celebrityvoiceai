from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder = "templates")
    app.config['SECRET_KEY'] = 'celebrityvoiceaisecretkey711999'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)
    
    login_manager = LoginManager() #create an instance of the login manager
    login_manager.login_view = 'auth.login' #if user is not logged in, redirect to login page
    login_manager.init_app(app) #initialize the login manager

    @login_manager.user_loader #this function will be called whenever a user is required
    def load_user(id):
        return User.query.get(int(id)) #get the user id

    return app

# Path: Website\main\__init__.py

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
    #check if the database exists, if not, create it
    #this is to avoid creating the database every time we run the app