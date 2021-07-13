import contextlib
import sys
from models.client.client import ClientModel
from models.client.confirmation import ConfirmationModel


def save_and_confirm_client(client_instance: ClientModel):
    """
    Saves a client instance to the db then creates and saves corresponding confirmation instance
    for the client instance saved.
    """
    client_instance.save_client_to_db()
    confirmation = ConfirmationModel(client_instance.id)
    confirmation.confirmed = True
    confirmation.save_to_db()


@contextlib.contextmanager
def client_ctxt_mngr(client_id):
    try:
        client = ClientModel.find_client_by_id(client_id)
        yield client
    except:
        client.rollback()
        return {'msg': sys.exc_info()}
        # raise
