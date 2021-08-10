import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailgunException
from libs.strings import gettext
from models.client.client import ClientModel
from models.business.business import BusinessModel
from models.shared_user.confirmation import ConfirmationModel
from schema.client.confirmation import ConfirmationSchema
from libs.user_helper import confirm_user

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, user_model_type: str, confirmation_id: str):
        return confirm_user(user_model_type, confirmation_id)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_model_type: str, email: str):
        """Return confirmations for a given client. Only for test purposes"""
        user = ClientModel.find_user_by_email(email) if user_model_type == 'client' else BusinessModel.find_user_by_email(email)
        if not user:
            return {'msg': gettext('confirmation_client_not_found')}, 404

        return {
            'current_time': int(time()),
            'confirmation': [
                confirmation_schema.dump(each)
                for each in user.confirmation.order_by(ConfirmationModel.expire_at)
            ],
        }, 200

    @classmethod
    def post(cls, user_model_type: str, email: str):  # email sent in POST body
        """Resend confirmation email"""
        user = ClientModel.find_user_by_email(email) if user_model_type == 'client' else BusinessModel.find_user_by_email(email)
        if not user:
            return {'msg': gettext('confirmation_client_not_found')}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {'msg': gettext('confirmation_already_confirmed')}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user)
            new_confirmation.save_to_db()

            user.send_verification_email()
            return {'msg': gettext('confirmation_email_resent_successful')}, 201
        except MailgunException as err:
            return str(err), 500
        except Exception as e:
            traceback.print_exc()
            return {
                'msg': gettext('confirmation_email_resend_failed'),
                'error_message': str(e)
            }, 404
