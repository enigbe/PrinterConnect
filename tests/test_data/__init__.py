# Client SignUp POST Request Details
client = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'password': '12345678'
}

expected_client = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'oauth_token': 'empty',
    'oauth_token_secret': 'empty',
    'id': 1
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
