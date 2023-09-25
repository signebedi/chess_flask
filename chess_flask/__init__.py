from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
db = SQLAlchemy(app)

# Setup logging
logging.basicConfig(filename='chess.log', level=logging.INFO)