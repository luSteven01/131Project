#import flask
#requires use to run flask.Flask(...)
#from library flask import the class Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
pathName = os.path.abspath(os.path.dirname(__file__))

obj = Flask(__name__)

obj.config.from_mapping(
    SECRET_KEY='im-batman',

    #where the database file is stored
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(pathName, 'app.db')

)
db = SQLAlchemy(obj)

from app import routes
