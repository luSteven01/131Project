from app import Usersdb
class User():
    id = Usersdb.Column(Usersdb.Integer, primary_key=True)
    name = Usersdb.Column(Usersdb.String(64), unique=True)
    email = Usersdb.Column(Usersdb.String(64))
