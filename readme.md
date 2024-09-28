<h1 align="center">REST API Authentification Microservice</h1>

<p align="center">
    <img src="https://img.shields.io/badge/%20Python-3.11.3-blue?style=for-the-badge&logo=Python" alt="Python">
    <img src="https://img.shields.io/badge/%20SQLAlchemy-2.0.35-brightgreen?style=for-the-badge" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/%20FastAPI-0.114.2-brightgreen?style=for-the-badge" alt="FastAPI">
    <img src="https://img.shields.io/badge/%20PyJWT- 2.9.0-brightgreen?style=for-the-badge" alt="20PyJWT">
    <img src="https://img.shields.io/badge/Passlib- 1.7.4-brightgreen?style=for-the-badge" alt="Passlib">
</p>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/rest-auth/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/rest-auth" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/rest-auth" alt="stars">
</p>

<h2>About</h2>

**_The application is designed to study microservice architecture and consider the interaction of services with each other via REST API with help of FastAPI and Pydantic frameworks. Also, for access remote microservicess used third-party library: requests._**

**_User authorization is implemented using JWT Tokens (PyJWT), work with the database is implemented using SQLAlchemy and SQLite._**
**_For password hashing used passlib library with bcrypt encryption_**

<h2>Deploy</h2>

- _Install Docker_
- _Create or download docker-compose file in any directory_: 
    - _Download latest release from my GitHub repository and take docker-compose.yml from it_
    - <details>
        <summary>
            Create file yourself, just put code below in empty file named 'docker-compose.yml
        </summary>

            version: '3'
            services:
                
                gateway:
                image: neitendo/rest-auth-gateway
                container_name: rest-auth-gateway
                restart: always
                build: ./gateway
                environment:
                    - REGISTRATION_SERVICE=http://reg:8001/reg
                    - AUTHENTIFICATION_SERVICE=http://reg:8001/auth
                    - TOKEN_VERIFYING_SERVICE=http://reg:8001/verify_token
                    - GET_USER_DATA_SERVICE=http://reg:8001/user
                command: uvicorn app.api:app --host 0.0.0.0 --port 8000
                ports:
                    - 8000:8000

            reg:
                image: neitendo/rest-auth-reg
                container_name: rest-auth-reg
                restart: always
                build: ./registration
                environment:
                    - JWT_SECRET=some_secret_value
                command: uvicorn app.api:app --host 0.0.0.0 --port 8001
                ports:
                    - 8001:8001
                depends_on:
                    - gateway
        
        </details>
- _Open terminal where your docker-compose file and run command:_ ```docker-compose run```

<br/>

> Good luck. Or you want API description?

<h2>API DOCS</h2>

```
Register new user: POST /reg 
Request schema: JSON

    {
        "name": "string",
        "email": "test@example.com",
        "password": "string"
    }
    
Response schema: JSON. Code 201
    
    {
        "result": "created"
    }
```

```
Authentificate: POST /auth
Request schema: JSON

    {
        "username": "string",
        "password": "string"
    }
    
Response schema: JSON. Code 200
    
    {
        "access_token": "token_string"
        "token_type": "bearer"
    }
```

```
Get current user data: GET /user
Response schema: JSON. Code 200
    
    {
        "id": 0
        "name": "current_user_name"
        "email": "current_user_email"
    }
```

>What else? That's all, I'm really lazy