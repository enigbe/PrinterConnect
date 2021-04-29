import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailgunException
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from schema.client.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()

NOT_FOUND = 'Confirmation reference for this account not found.'
EXPIRED = 'Account confirmation link has expired.'
USER_CONFIRMED = '{} activated successfully. You can now sign in.'
ALREADY_CONFIRMED = 'Client account already confirmed.'
CLIENT_NOT_FOUND = 'Client not found.'
EMAIL_RESEND_FAILED = 'Failed to resend verification email.'
VERIFICATION_EMAIL_RESENT = 'Verification email resent successfully.'


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {'msg': NOT_FOUND}, 404

        if confirmation.has_expired:
            return {'msg': EXPIRED}, 404

        if confirmation.confirmed:
            return {'msg': ALREADY_CONFIRMED}, 404

        confirmation.confirmed = True
        confirmation.save_to_db()

        return {'msg': USER_CONFIRMED.format(confirmation.client.email)}, 200


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, email):
        """Return confirmations for a given client. Only for test purposes"""
        client = ClientModel.find_client_by_email(email)
        if not client:
            return {'msg': CLIENT_NOT_FOUND}, 404

        return {
            'current_time': int(time()),
            'confirmation': [
                confirmation_schema.dump(each)
                for each in client.confirmation.order_by(ConfirmationModel.expire_at)
            ],
        }, 200

    @classmethod
    def post(cls, email: str):  # email sent in POST body
        """Resend confirmation email"""
        client = ClientModel.find_client_by_email(email)
        if not client:
            return {'msg': CLIENT_NOT_FOUND}, 404

        try:
            confirmation = client.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {'msg': ALREADY_CONFIRMED}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(client.id)
            new_confirmation.save_to_db()

            client.send_verification_email()
            return {'msg': VERIFICATION_EMAIL_RESENT}, 201
        except MailgunException as err:
            return str(err), 500
        except:
            traceback.print_exc()
            return {'msg': EMAIL_RESEND_FAILED}