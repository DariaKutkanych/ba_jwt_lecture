from flask_jwt import JWT
from settings import app, bcrypt, db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


def authenticate(email, password):
    user = User.query.filter(User.email == email).scalar()
    if bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


jwt = JWT(app, authenticate, identity)


if __name__ == '__main__':
    db.create_all()
