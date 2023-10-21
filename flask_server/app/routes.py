from flask import request, jsonify
from app import app, db
from app.models import Users

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/members')
def members():
    return jsonify({"members": ["Member1", "Member2", "Member3"]})

# Adds a new user and returns unique ID assigned to user
@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username not provided"}), 400

    user = Users(username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'username': user.username}), 201

@app.route('/user/<username>', methods=['GET'])
def get(username):
    user = Users.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    return jsonify({'id': user.id, 'username': user.username})

if __name__ == "__main__":
    app.run(debug=True)

