# Client SignUp POST Request Details
client = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'password': '12345678'
}

updated_client = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'bio': 'Bio updated'
}

client_profile = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'bio': None,
    'avatar_url': None
}

exp_client = {
    'first_name': 'jane',
    'username': 'jane_d',
    'last_name': 'doe',
    'avatar_filename': None,
    'avatar_url': None,
    'bio': None,
    'id': 1,
    'avatar_uploaded': False,
    'email': 'janedoe@email.com'
}


# Mailgun Email, Email Subject, and Email Text Details
class EmailDetails:
    email = ['ochekliyeenigbe@gmail.com']
    subject = 'Account Verification'
    text = 'Hello, your account has been verified.'


# Client SignIn POST Request Details
client_signin = {
    'email': 'janedoe@email.com',
    'password': '12345678'
}

# Github
github_authorized_response = {
    'status': 200,
    'access_token': 'access_token'
}

github_user_data = {
    'login': 'jane_d',
    'email': 'janedoe@enc.com',
    'name': 'Jane Doe'
}

twitter_user_data = {
    'email': 'janedoe@email.com',
    'screen_name': 'jane_d',
    'name': 'jane doe',
}

google_user_data = {
    'email': 'janedoe@email.com',
    'given_name': 'jane',
    'family_name': 'doe',
}

facebook_user_data = {
    'email': 'janedoe@email.com',
    'short_name': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
}

blocked_token = {'id': 1, 'jti': '1eb0f7f7-9c18-45c6-b297-15873258b328', 'client_id': 1}

searched_client = {
    'username': 'jane_d',
    'bio': None,
    'avatar_url':
    'http://localhost:5001/static/images/assets/default-avatar.png',
    'first_name': 'jane',
    'last_name': 'doe',
    'email': 'janedoe@email.com'
}
