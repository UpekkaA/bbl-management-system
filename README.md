# bbl-management-system
Basketball league  management system to monitor games statistics and rankings of a tournament

Simple JWT which is a JSON Web Token authentication plugin for the Django REST Framework is used to generate authentication tokens.

## Requirements
- Python 3.10.4
- Django 4.0.3
- Django REST Framework 3.13.1

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
cd bbl-management-system
python -m venv env
```

After this, it is necessary to activate the virtual environment.

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

Run Migrations
```
python manage.py migrate
```

Then, we have to start up Django's development server.
```
python manage.py runserver
```

First create the admin user 
```
python manage.py createsuperuser --email admin@example.com --username admin
```

## Create users and Tokens

First we need to create a user, so we can log in
All the admin users, coaches and players need to first register with the system.
```
http POST http://127.0.0.1:8000/api/v1/auth/register/ 
{
    "username": "victor",
    "password": "Bbl@4321",
    "email": "victor@bbltestdjango.com",
    "first_name": "Victor",
    "last_name": "Law"
}
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http http://127.0.0.1:8000/api/v1/auth/token/ 
{
    "username": "victor",
    "password": "Bbl@4321"
}
```
After that, we get the JWT token
this token can be used to access the API
Note: Some Read only calls are allowed to be accessed without a token
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTcwMjUzNiwiaWF0IjoxNjQ5NjE2MTM2LCJqdGkiOiI2NDE4N2M4NmE3YmE0NjM2YTg3OGI2NzljYjJlZTU2MSIsInVzZXJfaWQiOjZ9.LHymysJ89TpG2RF8XGm-W24BkQqHrIth6xexrTJWlRo",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NDM2LCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6IjUxOGMyN2VhYzUzODQ4NjViMDFmNmE4NzVkMDVlMmI3IiwidXNlcl9pZCI6Nn0.sGo__9ljkuWBVETrX8hzlqW7B_K9tmB0JECUDHd5Py8"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

requesting new access token
```
http http://127.0.0.1:8000/api/v1/auth/token/refresh/ 
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTcwMjUzNiwiaWF0IjoxNjQ5NjE2MTM2LCJqdGkiOiI2NDE4N2M4NmE3YmE0NjM2YTg3OGI2NzljYjJlZTU2MSIsInVzZXJfaWQiOjZ9.LHymysJ89TpG2RF8XGm-W24BkQqHrIth6xexrTJWlRo"
}
```
and we will get a new access token
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
}
```








