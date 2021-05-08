# Client SignUp POST Request Details
client = {
    'email': 'janedoe@email.com',
    'username': 'jane_d',
    'first_name': 'jane',
    'last_name': 'doe',
    'password': '12345678'
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
    'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
                    '.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjIwMjQzODQ2LCJ'
                    'qdGkiOiI2NWYyMjFjMy04NWZjLTQ4YjgtODA0MS0xNzV'
                    'hMDMyMGMzMjgiLCJuYmYiOjE2MjAyNDM4NDYsInR5cGU'
                    'iOiJhY2Nlc3MiLCJzdWIiOiJvY2hla2xpeWVlbmlnYmV'
                    'AZ21haWwuY29tIiwiZXhwIjoxNjIwMjQ0NzQ2fQ.7TOc'
                    '29v82N-1A4dP6-cuHwPQ06Qo3z4J8Ayxc7sq0HA '
}

github_user_data = {
    'email': 'janedoe@enc.com',
    'name': 'Jane Doe'
}
