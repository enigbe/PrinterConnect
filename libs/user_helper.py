import uuid
from typing import Dict

from flask_jwt_extended import create_access_token, create_refresh_token

from models.confirmation import ConfirmationModel
from models.business.business import BusinessModel
from models.client.client import ClientModel
from libs.strings import gettext
from libs.mailgun import MailgunException


def save_and_confirm_user(user_instance):
    """
    Saves a user (business or client) instance to the db then creates
    and saves corresponding confirmation instance for the user instance saved.
    """
    user_instance.save_user_to_db()
    confirmation = ConfirmationModel(user_instance)
    # confirmation.confirmed = True
    confirmation.save_to_db()


def generate_random_username():
    """Generate random username"""
    rand_name = str(uuid.uuid4().hex)[:10]
    return rand_name


def generate_random_email():
    """Generate random email address"""
    pre_symbol = str(uuid.uuid4().hex)[:10]
    post_symbol = 'email.com'
    return f'{pre_symbol}@{post_symbol}'


def generate_random_password():
    """Generate random 15 word password"""
    password = str(uuid.uuid4().hex)[:15]
    return password


def generate_random_id():
    """Generate random 4 digit integer"""
    return int(str(uuid.uuid4().int)[:4])


def signup_user_with_email(user_model, user_data: Dict) -> tuple:
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


def signin_user_with_email(user_model, user_data: Dict) -> tuple:
    user = user_model.find_user_by_email(user_data['email'])
    if user and user.verify_password(user_data['password']):
        confirmation = user.most_recent_confirmation
        if confirmation and confirmation.confirmed:
            # 4. If 3 above is true, generate an access and refresh token to access protected endpoints
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                       'msg': gettext('signin_successful'),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'msg': gettext('signin_account_not_confirmed')}, 401
    # 5. Return success message and tokens
    return {'msg': gettext('signin_invalid_credentials')}, 401


def confirm_user(user_model_type: str, confirmation_id: str):
    confirmation = ConfirmationModel.find_by_id(confirmation_id)

    if not confirmation:
        return {'msg': gettext('confirmation_not_found')}, 404

    if confirmation.has_expired:
        return {'msg': gettext('confirmation_expired')}, 404

    if confirmation.confirmed:
        return {'msg': gettext('confirmation_already_confirmed')}, 404

    confirmation.confirmed = True
    confirmation.save_to_db()

    user = BusinessModel.find_user_by_id(confirmation.business_id) \
        if user_model_type == 'business' \
        else ClientModel.find_user_by_id(confirmation.client_id)

    return {'msg': gettext('confirmation_successful').format(user.email)}, 200


def read_user(username, user_instance, full_user_schema, partial_user_schema, user_id: int = None):
    if user_instance is None:
        return {'msg': gettext('user_profile_does_not_exist').format(username)}, 400
    if user_instance.id == user_id:
        return {'business'
                if user_instance.__class__.__name__ == 'BusinessModel'
                else 'client': full_user_schema.dump(user_instance)}, 200

    return {'business'
            if user_instance.__class__.__name__ == 'BusinessModel'
            else 'client': partial_user_schema.dump(user_instance)}, 200


def delete_user(username, user_instance, user_id: int):
    if user_instance is None:
        return {'msg': gettext('user_profile_does_not_exist').format(username)}, 400

    if user_instance.id != user_id:
        return {'msg': gettext('user_profile_deletion_unauthorized')}, 403

    try:
        user_instance.delete_user_from_db()
        return {'msg': gettext('user_profile_client_deleted').format(user_instance.username)}, 200
    except Exception as e:
        user_instance.rollback()
        return {'msg': str(e)}, 500
