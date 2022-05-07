from flask import Flask

# Initializing application
app = Flask(__name__)
app.config['SECRET_KEY'] = '564648sjdhbfl654684adfa'

from app import views