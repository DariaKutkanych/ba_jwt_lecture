from flask import jsonify
from flask_jwt import jwt_required
from settings import app
from models import User


@app.route('/users')
@jwt_required()
def get_users():
    return jsonify({"users": [u.serialize() for u in User.query.all()]}), 200


if __name__ == '__main__':
    app.run()
