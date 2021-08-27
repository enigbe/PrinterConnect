from libs.user_helper import (
    generate_random_username,
    generate_random_email,
    generate_random_password,
    generate_random_id,
    generate_random_item
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
successful_update = {'msg': 'User profile updated successfully'}

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
    'id': 1, 'jti': '1eb0f7f7-9c18-45c6-b297-15873258b328', 'client_id': 1, 'business_id': None}

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
    # 'cad_object_key': 'client_1/Test CAD Model'
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

# Business details
business_data = {
    'id': generate_random_id(),
    'business_name': generate_random_username(),
    'email': generate_random_email(),
    'username': generate_random_username(),
    'password': generate_random_password(),
    'bio': generate_random_username()
}
update_business_data = {
    'business_name': generate_random_username(),
    'email': generate_random_email(),
    'username': generate_random_username(),
    'password': generate_random_password(),
    'bio': generate_random_username()
}

# Printer details
print_materials = ('PLA', 'ABS', 'ASA', 'HIPS', 'PETG', 'NYLON', 'CFF', 'PCB', 'PVA',)
print_file_types = ('STL', 'OBJ', 'AMF', '_3MF', 'PLY', 'STEP', 'IGES')
printer_data = {
    "id": generate_random_id(),
    "name": generate_random_username(),
    "model": generate_random_username(),
    "base_width": generate_random_id(),
    "base_length": generate_random_id(),
    "height": generate_random_id(),
    "nozzle_diameter": generate_random_id(),
    "file_type": generate_random_item(print_file_types),  # Enum (printer_file_type) of 5 popular file types
    "material": generate_random_item(print_materials)  # Enum (printer_material) of 10 popular materials
}
printer_update_data = {
    "id": generate_random_id(),
    "name": generate_random_username(),
    "model": generate_random_username(),
    "base_width": generate_random_id(),
    "base_length": generate_random_id(),
    "height": generate_random_id(),
    "nozzle_diameter": generate_random_id(),
    "file_type": generate_random_item(print_file_types),  # Enum (printer_file_type) of 5 popular file types
    "material": generate_random_item(print_materials)  # Enum (printer_material) of 10 popular materials
}

