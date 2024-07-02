# FastAPI Authentication and Authorization

This project implements a basic authentication and authorization system using FastAPI, SQLAlchemy, and JWT. It supports user registration, login, and token management (access and refresh tokens).

## Project Structure

```plaintext
.
├── app
│   ├── __init__.py        # Initializes the app as a package
│   ├── server.py          # Setup routes, middleware, and other server configurations
├── auth
│   ├── __init__.py
│   ├── models.py          # Database models, including User and RefreshToken
│   ├── schemas            # Pydantic schemas for request and response models, including user and token schemas
│   │   ├── token.py
│   │   └── user.py
│   ├── dao.py             # Data Access Object for handling database operations
│   ├── dependencies.py    # Dependency injection for routes, including current user retrieval
│   ├── router.py          # API routers for handling authentication-related endpoints
│   └── utils.py           # Utility functions for auth like password hashing and token generation
├── db
│   ├── __init__.py
│   └── connection.py      # Database connection setup using SQLAlchemy
├── config
│   ├── __init__.py
│   └── settings.py        # Configuration settings using pydantic-settings
├── Dockerfile             # Dockerfile for containerizing the application
├── docker-compose.yaml    # Docker Compose file for setting up the development environment
├── main.py                # Main application setup
└── README.md              # Project documentation
```

## Features

```plaintext
- User registration
- User login
- JWT access and refresh token generation
- Endpoint security with token verification
- Access and Refresh token generation
- Revoke the refresh token
- Swagger documentation
```

## Prerequisites
```plaintext
- Python 3.9+
- Docker & Docker Compose
- FastAPI
- SQLAlchemy
- Uvicorn (ASGI server)
- JWT token handling (python-jose)
- Password hashing (passlib)
```

## Quick Start
You can use Docker to quickly start the application. The APIs will be available on the Swagger endpoint: localhost:8000/docs.
```plaintext
docker-compose up -d
```

## CURL Requests

### Register User
```commandline
curl --location --request POST 'http://localhost:8000/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "prathmeshingole20@gmail.com",
  "password": "Pass123@$"
}'

```

### Login User
```commandline
curl --location --request POST 'http://localhost:8000/auth/login' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=prathmeshingole20@gmail.com' \
--data-urlencode 'password=Pass123@$'
```

### Refresh Access Token
```commandline
curl --location --request POST 'http://localhost:8000/auth/token/refresh?refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmF0aG1lc2hpbmdvbGUyMEBnbWFpbC5jb20iLCJpYXQiOjE3MTk5NDQ3MTUsIm5vbmNlIjoiZjY5ZjE2MWY0MTMyNjI4M2IyMGVmZjgzMzZiMzE3ODMifQ.WY35XG4mXhROL3AxoX0XUuazIZIGwTDOEtQuWLgTGNY' \
--data-raw ''
```


### Get Current User Details
```commandline
curl --location --request GET 'http://localhost:8000/auth/users/me' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmF0aG1lc2hpbmdvbGUyMEBnbWFpbC5jb20iLCJleHAiOjE3MTk5NDY1MTV9.IDuULYqPmAzu8f_wO314T1HfOSNVqjn4asIGLsI9eQM' \
--data-raw ''

```


### Revoke Token
```commandline
curl --location --request POST 'http://localhost:8000/auth/token/revoke?refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmF0aG1lc2hpbmdvbGUyMEBnbWFpbC5jb20iLCJpYXQiOjE3MTk5NDQ3MTUsIm5vbmNlIjoiZjY5ZjE2MWY0MTMyNjI4M2IyMGVmZjgzMzZiMzE3ODMifQ.WY35XG4mXhROL3AxoX0XUuazIZIGwTDOEtQuWLgTGNY' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwcmF0aG1lc2hpbmdvbGUyMEBnbWFpbC5jb20iLCJleHAiOjE3MTk5NDU2Njl9.nAKEtEU2TP5wG8PEauwCGq-HU0lZ2VM8FnFClCSI2lU' \
--data-raw ''

```


