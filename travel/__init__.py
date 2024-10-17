from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    Bootstrap5(app)

    app.secret_key = 'somerandomvalue'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app