#import flask

from flask import Flask

obj = Flask(__name__)

from app import routes
