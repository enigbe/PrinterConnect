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
