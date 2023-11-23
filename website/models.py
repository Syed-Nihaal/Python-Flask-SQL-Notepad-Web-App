# Imports modules from packages
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Defines the Note model
class Note(db.Model):
    # Primary key for the Note model
    id = db.Column(db.Integer, primary_key=True)
    # Column for storing the actual data of the note
    data = db.Column(db.String(10000))
    # Foreign key relationship for associating a note with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Defines the User model
class User(db.Model, UserMixin):
    # Primary key for the User model
    id = db.Column(db.Integer, primary_key=True)
    # Column for storing the user's email
    email = db.Column(db.String(150), unique=True)
     # Column for storing the hashed password of the user
    password = db.Column(db.String(150))
    # Relationship for linking a user with their notes
    notes = db.relationship('Note')