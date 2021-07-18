import uuid
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
