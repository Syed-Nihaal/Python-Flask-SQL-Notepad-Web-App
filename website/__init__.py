# Imports modules from packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize the SQLAlchemy database object
db = SQLAlchemy()
# Define the name of the database file
DB_NAME = "webapp.db"

# Function for creating the Flask application
def create_app():
    # Create a Flask application instance
    app = Flask(__name__)
    # Configure the application with a secret key and SQLite database URI
    app.config["SECRET_KEY"] = "123456789"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # Initializing the SQLAlchemy database with the Flask application
    db.init_app(app)

    # Import and register blueprints for different views and authentication
    from .views import views
    from .authenticate import authenticate
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(authenticate, url_prefix="/")

    # Import the User and Note models and create the database tables
    from .models import User, Note
    with app.app_context():
        db.create_all()

    # Initialize the Flask-Login extension
    login_manager = LoginManager()
    login_manager.login_view = "authenticate.login"  # Set the login view for redirection
    login_manager.init_app(app)

    # Function for loading a user from the database based on the user ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the configured Flask application
    return app

# Function for creating the database if it doesn't exist
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)  # Create all tables defined in the models
        print("Database created")

# Creating the Flask application
if __name__ == '__main__':
    app = create_app()
    # Creating the database if it doesn't exist
    create_database(app)