from libs.client_helper import (
    generate_random_username,
    generate_random_email,
    generate_random_password,
    generate_random_id
)
# Client SignUp POST Request Details
client = {
    'id': generate_random_id(),
    'email': generate_random_email(),
    'username': generate_random_username(),
    'first_name': 'jane',
    'last_name': 'doe',
    'password': generate_random_password()
}

updated_client_data = {
    'bio': 'Bio updated'
}

client_profile = {
    'email': generate_random_email(),
    'username': generate_random_username(),
    'first_name': 'jane',
    'last_name': 'doe',
    'bio': None,
    'avatar_url': None
}

exp_client = {
    'email': generate_random_email(),
    'username': generate_random_username(),
    'last_name': 'doe',
    'avatar_filename': None,
    'avatar_url': None,
    'bio': None,
    'id': 1,
    'avatar_uploaded': False,
}


# Mailgun Email, Email Subject, and Email Text Details
class EmailDetails:
    email = [generate_random_email()]
    subject = 'Account Verification'
    text = 'Hello, your account has been verified.'


# Client SignIn POST Request Details
client_signin = {
    'email': generate_random_email(),
    'password': generate_random_password()
}

# Github
github_authorized_response = {
    'status': 200,
    'access_token': 'access_token'
}

github_user_data = {
    'login': generate_random_username(),
    'email': generate_random_email(),
    'name': 'Jane Doe'
}

twitter_user_data = {
    'email': generate_random_email(),
    'screen_name': generate_random_username(),
    'name': 'jane doe',
}

google_user_data = {
    'email': generate_random_email(),
    'given_name': 'jane',
    'family_name': 'doe',
}

facebook_user_data = {
    'email': generate_random_email(),
    'short_name': generate_random_username(),
    'first_name': 'jane',
    'last_name': 'doe',
}

blocked_token = {
    'id': 1, 'jti': '1eb0f7f7-9c18-45c6-b297-15873258b328', 'client_id': 1}

searched_client = {
    'username': generate_random_username(),
    'bio': None,
    'avatar_url':
    'http://localhost:5001/static/images/assets/default-avatar.png',
    'first_name': 'jane',
    'last_name': 'doe',
    'email': generate_random_email()
}

cad_model_data = {
    'cad_model_name': 'Test CAD Model',
    'cad_model_height': 12.5,
    'cad_model_length': 12.5,
    'cad_model_width': 12.5,
    'cad_model_visibility': True,
    'cad_model_material': 'PLA',
    'cad_model_mesh_percent': 50,
    'cad_object_key': 'client_1/Test CAD Model'
}
cad_model_update_data = {
    'cad_model_name': 'Test CAD Model',
    'cad_model_height': 15,
    'cad_model_length': 15,
    'cad_model_width': 15,
    'cad_model_visibility': False,
    'cad_model_material': 'ABS',
    'cad_model_mesh_percent': 25,
}
