from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


app = Flask(__name__)
CORS(app, origins="*")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clarium.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
