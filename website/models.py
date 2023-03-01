from . import db # Importing the database
from flask_login import UserMixin # helps us to manage users login
from sqlalchemy.sql import func # helps us to manage the date
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key to help us identify each note
    data = db.Column(db.String(10000)) # the actual note
    date = db.Column(db.DateTime(timezone = True), default=func.now()) # the date the note was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # the user who created the note
    date_timer = db.Column(db.DateTime(timezone = True), default=func.now()) # the date the note was created

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary key to help us identify each user
    email = db.Column(db.String(150), unique=True) # unique email address
    first_name = db.Column(db.String(150)) 
    password = db.Column(db.String(150))
    # password2 = db.Column(db.String(150))
    notes = db.relationship('Note') # relationship between the user and the note

class Persona(db.Model,Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_url = Column(String)
    short_description = Column(String)

    def __init__(self, name, image_url, short_description):
        self.name = name #name of the persona
        self.image_url = image_url #image_url is the image of the persona
        self.short_description = short_description #short_description is the image of the persona
