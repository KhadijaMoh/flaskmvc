import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
# Try importing secure_filename from werkzeug.utils explicitly
from werkzeug.utils import secure_filename, FileStorage
# If the above doesn't work, try this alternative import:
# from werkzeug import secure_filename, FileStorage

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin

# Initialize Flask-SQLAlchemy and Flask-Login
db = SQLAlchemy()
login_manager = LoginManager()

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)

    # Initialize Flask-SQLAlchemy and Flask-Login with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # You'll define this in your auth blueprint

    from .app.models.user import User  # Import here to avoid circular dependency

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    # Import blueprints here to avoid circular dependencies
    from .auth.routes import auth_bp
    from .apartments.routes import apartments_bp
    from .reviews.routes import reviews_bp

    # Register your blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(apartments_bp, url_prefix='/apartments')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    with app.app_context():
        db.create_all() # Create database tables

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)