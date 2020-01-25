from flask import request, jsonify
from settings import app, bcrypt, db
from models import User


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user:
        return jsonify({'message': 'User already exists'}), 200

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    db.session.add(user)
    db.session.commit()

    token = user.encode_auth_token()
    return jsonify({"auth_token": token.decode()}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get('email')).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = user.encode_auth_token()
        return jsonify({"auth_token": token.decode()}), 201

    return jsonify({"message": "User does not exist"}), 404


@app.route('/users')
def get_users():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]

    result = User.decode_auth_token(token)
    if not isinstance(result, str):
        return jsonify(
            {"users": [u.serialize() for u in User.query.all()]}
        ), 200

    return jsonify({"message": result}), 401


if __name__ == '__main__':
    app.run()
