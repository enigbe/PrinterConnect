import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailgunException
from libs.strings import gettext
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel
from schema.client.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {'msg': gettext('confirmation_not_found')}, 404

        if confirmation.has_expired:
            return {'msg': gettext('confirmation_expired')}, 404

        if confirmation.confirmed:
            return {'msg': gettext('confirmation_already_confirmed')}, 404

        confirmation.confirmed = True
        confirmation.save_to_db()

        return {'msg': gettext('confirmation_successful').format(confirmation.client.email)}, 200


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, email):
        """Return confirmations for a given client. Only for test purposes"""
        client = ClientModel.find_client_by_email(email)
        if not client:
            return {'msg': gettext('confirmation_client_not_found')}, 404

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
            return {'msg': gettext('confirmation_client_not_found')}, 404

        try:
            confirmation = client.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {'msg': gettext('confirmation_already_confirmed')}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(client.id)
            new_confirmation.save_to_db()

            client.send_verification_email()
            return {'msg': gettext('confirmation_email_resent_successful')}, 201
        except MailgunException as err:
            return str(err), 500
        except Exception as e:
            traceback.print_exc()
            return {
                'msg': gettext('confirmation_email_resend_failed'),
                'error_message': str(e)
            }, 404
