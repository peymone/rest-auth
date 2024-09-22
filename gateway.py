from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
import uvicorn

from typing import Annotated
from configparser import ConfigParser

from models import *


app = FastAPI()
oauth2_cheme = OAuth2PasswordBearer(tokenUrl='auth')


@app.post('/reg', status_code=status.HTTP_201_CREATED)
async def register(user: UserReg) -> HTTPError:
    """Register user by invoking specific service via HTTP (RestAPI)"""

    # Send user data to registration service. Receive access_token
    response = requests.post(REGISTRATION, json=user.model_dump(), timeout=10)
    response = response.json()

    if response['user_id'] is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="transaction failed when creating a user")
    else:
        return RedirectResponse('/user')


@app.post('/auth')
async def authentificate(form_data: OAuth2PasswordRequestForm = Depends()) -> Token | HTTPError:
    """Authentificate User and return JWT token"""

    # Get user data from oauth form and send request to authentification service
    user_data = {'name': form_data.username, 'password': form_data.password}
    response = requests.post(AUTHENTIFICATION, json=user_data)
    response = response.json()

    # Get JWT token and send to client
    if response['access_token'] is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email")
    else:
        return response


@app.get('/user')
async def get_current_user(token: Annotated[str, Depends(oauth2_cheme)]) -> UserGet | HTTPError:
    """Verify JWT Token and return current logged id user"""

    # Verify JWT token and get user id
    response = requests.post(TOKEN_VERIFYING, json={'access_token': token})
    response = response.json()
    user_id = response['user_id']

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # Get user data from specific service and return it
    response = requests.get(GET_USER_DATA, params={'user_id': user_id})
    response = response.json()

    if response['user_data'] is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    else:
        return response


if __name__ == '__main__':

    # Load config from settings.ini
    config = ConfigParser()
    config.read('settings.ini')

    REGISTRATION = config['links']['REGISTRATION_SERVICE']
    AUTHENTIFICATION = config['links']['AUTHENTIFICATION_SERVICE']
    TOKEN_VERIFYING = config['links']['TOKEN_VERIFYING_SERVICE']
    GET_USER_DATA = config['links']['GET_USER_DATA_SERVICE']

    uvicorn.run(app, host='localhost', port=8001)
