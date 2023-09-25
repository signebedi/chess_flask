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



@app.route('/game', methods=['POST'])
def create_game():
    game = Game(turn='w')
    db.session.add(game)
    db.session.commit()
    logging.info(f'Game {game.id} created.')
    return jsonify({'game_id': game.id}), 201

@app.route('/game/<int:game_id>/move', methods=['PUT'])
def make_move(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    req_data = request.get_json()
    move_uci = req_data.get('move')
    player = req_data.get('player')

    if player != game.turn:
        return jsonify({'error': "Not player's turn"}), 403

    board = chess.Board()
    for move in game.moves:
        board.push_uci(move.uci)

    try:
        board.push_uci(move_uci)
    except ValueError:
        return jsonify({'error': 'Invalid move'}), 400

    move = Move(uci=move_uci, game=game)
    game.turn = 'b' if game.turn == 'w' else 'w'  # alternate turn
    db.session.add(move)
    db.session.commit()
    logging.info(f'Move made in game {game_id}: {move_uci}')
    return jsonify({'status': 'Move made'}), 200

@app.route('/game/<int:game_id>/moves', methods=['GET'])
def get_moves(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify({'moves': [move.uci for move in game.moves]}), 200

@app.route('/game/<int:game_id>/position/<int:move_number>', methods=['GET'])
def get_position(game_id, move_number):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    board = chess.Board()
    for move in game.moves[:move_number]:
        board.push_uci(move.uci)

    return jsonify({'position': board.fen()}), 200

if __name__ == '__main__':
    app.run(debug=True)