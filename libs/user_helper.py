import uuid
from typing import Dict

from models.client.client import ClientModel
from models.business.business import BusinessModel
from models.client.confirmation import ConfirmationModel
from libs.strings import gettext
from libs.mailgun import MailgunException


def save_and_confirm_user(user_instance: [ClientModel, BusinessModel]):
    """
    Saves a client instance to the db then creates and saves corresponding confirmation instance
    for the client instance saved.
    """
    user_instance.save_user_to_db()
    confirmation = ConfirmationModel(user_instance)
    confirmation.confirmed = True
    confirmation.save_to_db()


def generate_random_username():
    rand_name = str(uuid.uuid4().hex)[:10]
    return rand_name


def generate_random_email():
    pre_symbol = str(uuid.uuid4().hex)[:10]
    post_symbol = 'email.com'
    return f'{pre_symbol}@{post_symbol}'


def generate_random_password():
    password = str(uuid.uuid4().hex)[:15]
    return password


def generate_random_id():
    return int(str(uuid.uuid4().int)[:4])


def signup_user_with_email(user_model: [BusinessModel, ClientModel], user_data: Dict) -> tuple:
    """
    Creates a new user (business or client) account given the user model and
    registration data
    :param user_model: Either a BusinessModel or a ClientModel
    :param user_data: A validated user data for account creation
    """
    username = user_data['username'] or None
    email = user_data['email'] or None

    if user_model.find_user_by_email(email):
        return {'msg': gettext('signup_email_already_exists').format(email)}, 400
    elif user_model.find_user_by_username(username):
        return {'msg': gettext('signup_username_already_exists').format(username)}, 400
    else:
        try:
            user = user_model(**user_data)
            user.hash_password(user.password)
            save_and_confirm_user(user)
            user.send_verification_email()
        except MailgunException as err:
            user.delete_user_from_db()
            return {'msg': str(err)}, 500
        except Exception as err:
            return {'msg': gettext('signup_account_creation_failed'), 'exception': str(err)}, 500
        else:
            return {'msg': gettext('signup_account_creation_successful')}, 201
