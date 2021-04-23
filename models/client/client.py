from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class ClientModel(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    username = db.Column(db.String(120), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email: str, username: str, first_name: str, last_name: str, password: str) -> None:
        self.email = email
        self.username = username
        self.first_name = first_name[0].upper() + first_name[1:].lower()
        self.last_name = last_name[0].upper() + last_name[1:].lower()
        self.password = generate_password_hash(password)

    def __repr__(self) -> str:
        return '<Client => {} {}: [@{} - ({})]>'.format(self.first_name, self.last_name, self.username, self.email)

    @classmethod
    def find_client_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_client_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def save_client_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_client_from_db(self):
        db.session.delete(self)
        db.session.commit()
