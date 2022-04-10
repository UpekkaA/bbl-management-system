# bbl-management-system

Basketball league management system to monitor games statistics and rankings of a tournament

Simple JWT which is a JSON Web Token authentication plugin for the Django REST Framework is used to generate
authentication tokens.

## Requirements

- Python 3.10.4
- Django 4.0.3
- Django REST Framework 3.13.1
- djangorestframework-simplejwt 5.1.0
- django-filter 2.4.0
- numpy 1.22.3
- pandas 1.4.2

## Installation

After you cloned the repository, you want to create a virtual environment

```
cd bbl-management-system
python -m venv env
```

You can install all the required dependencies by running

```
pip install -r requirements.txt
```

Run Migrations

```
python manage.py migrate
```

First create the admin user

```
python manage.py createsuperuser --email admin@example.com --username admin
```

Then, we have to start up Django's development server.

```
python manage.py runserver
```

## Create Users and Tokens

First we need to create a user, so we can log in All the admin users, coaches and players need to first register with
the system.

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

After that, we get the JWT token this token can be used to access the API Note: Some Read only calls are allowed to be
accessed without a token

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTcwMjUzNiwiaWF0IjoxNjQ5NjE2MTM2LCJqdGkiOiI2NDE4N2M4NmE3YmE0NjM2YTg3OGI2NzljYjJlZTU2MSIsInVzZXJfaWQiOjZ9.LHymysJ89TpG2RF8XGm-W24BkQqHrIth6xexrTJWlRo",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NDM2LCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6IjUxOGMyN2VhYzUzODQ4NjViMDFmNmE4NzVkMDVlMmI3IiwidXNlcl9pZCI6Nn0.sGo__9ljkuWBVETrX8hzlqW7B_K9tmB0JECUDHd5Py8"
}
```

We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token
will expire after some time. We can use the refresh token to request a need access token.

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

Update user with PUT/PATCH

```
PUT http://127.0.0.1:8000/api/v1/auth/users/2/
{
    "username": "victor",
    "password": "pbkdf2_sha256$320000$HjyVmaVrWHqdjRYLD1KREy$aHuajYO8DDwT32ULPKj8XuSgAl0x7FlFdKJg+zgCbYI=",
    "email": "victor@bbltestdjango.com",
    "first_name": "Victor",
    "last_name": "Lawrence",
    "groups": []
}
```

Create Groups which will be used for Permission handling

```
POST http://127.0.0.1:8000/api/v1/auth/groups/
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"

{
    "name":"PLAYER"
}
```

Get Groups

```
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
GET http://127.0.0.1:8000/api/v1/auth/groups/
Sample Response:
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "PLAYER"
        },
        {
            "id": 2,
            "name": "COACH"
        },
        {
            "id": 3,
            "name": "ADMIN"
        }
    ]
}
```

# Teams

Create Teams

```
POST http://127.0.0.1:8000/api/v1/league/teams
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
{
    "name":"Tasmania JackJumpers",
    "logo_url":"https://source.unsplash.com/user/c_v_r/100x100"
}
```

Get Teams

```
GET http://127.0.0.1:8000/api/v1/league/teams
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
Sample Response:
{
    "count": 16,
    "next": "http://127.0.0.1:8000/api/v1/league/teams?page=2&page_size=5",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Tasmania JackJumpers",
            "logo_url": "https://source.unsplash.com/user/c_v_r/100x100",
            "creator": "admin"
        }
    ]
}
```

Also support PUT/PATCH Operations

# Coach

Create Coach

```
POST http://127.0.0.1:8000/api/v1/league/coaches
{
  "user": 2,
  "team": 1
}
```

# Player

Create Player

```
POST http://127.0.0.1:8000/api/v1/league/players
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
{
  "user": 3,
  "team": 1
}
```

Update Player

```
PUT http://127.0.0.1:8000/api/v1/league/players/1/
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
{
    "user": 3,
    "team": 1,
    "height": 190,
    "games_played": 10,
    "points_total": 200,
    "points_average": 80.3
}
```

Get Players

```
GET http://127.0.0.1:8000/api/v1/league/players?team=1&games_played_gt=5&points_total_gt=100&user_name=john&page_size=5&page=1
Query parameters are optional
Sample Response:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "user": 3,
            "team": 1,
            "height": 190,
            "games_played": 10,
            "points_total": 200,
            "points_average": 80.3,
            "username": "John",
            "first_name": "John",
            "last_name": "Doe",
            "team_name": "Brisbane Bullets"
        }
    ]
}
```

# Stadium

Create Stadium

```
POST http://127.0.0.1:8000/api/v1/league/stadiums
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
{
    "name": "Adelaide Ground",
    "location": "Adelaide, Australia"
}
```

# Game

Create Game

```
POST http://127.0.0.1:8000/api/v1/league/games
"Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NjE2NjYwLCJpYXQiOjE2NDk2MTYxMzYsImp0aSI6ImQxOGM2MjQ5ODgwODQ5NTJhNDQxOGNkNDc5NTU2NDNhIiwidXNlcl9pZCI6Nn0.tthmS9FQZPj27kRdyd85FpRlgrIe-1kxKGRIzkJaFLg"
{
  "date_time": "2022-05-10 08:00:00.000000",
  "stadium": 1,
  "finished": false,
  "round": "QU",
  "team_home": 1,
  "team_away": 2
}
```

Get Games

```
GET http://127.0.0.1:8000/api/v1/league/games
Sample Response
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "date_time": "2022-05-11T08:00:00Z",
            "stadium": 1,
            "finished": true,
            "round": "QU",
            "team_home": 1,
            "team_away": 2,
            "winner": 1,
            "score_home": 12,
            "score_away": 10,
            "creator": "admin"
        }
    ]
}
```

# Notes

Refer the db_dump folder with sample data. Import data to relevant tables

TODO:

Permission Handling

Team Selection

Statistics of the site’s usage

# References

https://www.django-rest-framework.org/tutorial/quickstart/

https://github.com/juanbenitezdev/django-rest-framework-crud

https://rapidapi.com/api-sports/api/api-basketball/








