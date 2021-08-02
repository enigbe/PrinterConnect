import abc
from abc import ABCMeta, abstractmethod

from flask_sqlalchemy.model import DefaultMeta

from data_base import db
from requests import Response


class UserModel(metaclass=ABCMeta):
    def __repr__(self):
        return f'<UserModel>'

    def save_user_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update_user_in_db() -> None:
        db.session.commit()

    def delete_user_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

    @abstractmethod
    def hash_password(self, password: str): pass

    @abstractmethod
    def verify_password(self, password: str): pass

    @abstractmethod
    def send_verification_email(self) -> Response: pass

    @abstractmethod
    def send_update_email_notification(self, new_email) -> Response: pass

    @abstractmethod
    def send_password_reset_link(self) -> Response: pass

    @classmethod
    @abstractmethod
    def find_user_by_id(cls, _id: int) -> 'UserModel': pass

    @classmethod
    @abstractmethod
    def find_user_by_email(cls, email: str) -> 'UserModel': pass

    @classmethod
    @abstractmethod
    def find_user_by_username(cls, username: str) -> 'UserModel': pass


class DBModelUserModel(DefaultMeta, abc.ABCMeta):
    """Fix metaclass conflict"""
    pass
