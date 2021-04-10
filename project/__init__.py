from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'fasdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(username):
        """Load user from Astra by username, load into User object
        
        current_user calls this function
        """
        user = User()
        user.username = username
        user.password = "test"
        ## add all data from astra for this user
        
        return user

    return app

    