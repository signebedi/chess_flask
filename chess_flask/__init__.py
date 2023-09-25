from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging, chess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
db = SQLAlchemy(app)

# Setup logging
logging.basicConfig(filename='chess.log', level=logging.INFO)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn = db.Column(db.String(1))  # 'w' or 'b'
    moves = db.relationship('Move', backref='game')

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uci = db.Column(db.String(10))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

db.create_all()