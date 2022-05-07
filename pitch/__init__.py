from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager






app = Flask(__name__)
app.config['SECRET_KEY'] = '564648sjdhbfl654684adfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from pitch import routes